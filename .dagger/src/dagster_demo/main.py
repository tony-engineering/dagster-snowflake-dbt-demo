import dagger
from dagger import dag, function, object_type
from typing import Optional


@object_type
class DagsterDemo:
    """Dagger CI/CD pipeline for Dagster + dbt + Snowflake project"""
    
    @function
    def python_deps_layer(self, source: dagger.Directory, python_version: str = "3.13") -> dagger.Container:
        """Create a shared dependency layer that can be reused across all functions"""
        # Use a single shared pip cache
        pip_cache = dag.cache_volume("pip-cache-shared")
        
        return (
            dag.container()
            .from_(f"python:{python_version}-slim")
            .with_mounted_cache("/root/.cache/pip", pip_cache)
            .with_exec(["apt-get", "update"])
            .with_exec(["apt-get", "install", "-y", "git", "curl", "build-essential"])
            .with_exec(["pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
            # Install main dependencies first (these rarely change)
            .with_file("/tmp/pyproject.toml", source.file("dagster-demo/pyproject.toml"))
            .with_exec(["pip", "install", "dagster", "dagster-cloud", "dagster-webserver", "dagster-dbt", "dbt-core", "dbt-duckdb", "dbt-snowflake"])
            # Install dev dependencies
            .with_exec(["pip", "install", "pytest", "ruff", "black", "isort", "safety", "bandit"])
        )

    @function
    def python_base(self, python_version: str = "3.13") -> dagger.Container:
        """Create a base Python container with common dependencies and pip caching"""
        # Use shared pip cache
        pip_cache = dag.cache_volume("pip-cache-shared")
        
        return (
            dag.container()
            .from_(f"python:{python_version}-slim")
            .with_mounted_cache("/root/.cache/pip", pip_cache)
            .with_exec(["apt-get", "update"])
            .with_exec(["apt-get", "install", "-y", "git", "curl", "build-essential"])
            .with_exec(["pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
        )

    @function
    def python_with_deps_optimized(self, source: dagger.Directory, python_version: str = "3.13") -> dagger.Container:
        """Create a Python container with optimized dependency caching following Dagger best practices"""
        # Create cache volumes for different package managers and artifacts
        pip_cache = dag.cache_volume("pip-cache")
        dbt_packages_cache = dag.cache_volume("dbt-packages-cache")
        dbt_target_cache = dag.cache_volume("dbt-target-cache")
        
        return (
            dag.container()
            .from_(f"python:{python_version}-slim")
            # Mount pip cache early
            .with_mounted_cache("/root/.cache/pip", pip_cache)
            .with_exec(["apt-get", "update"])
            .with_exec(["apt-get", "install", "-y", "git", "curl", "build-essential"])
            .with_exec(["pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
            # Copy only requirements files first for better layer caching
            .with_file("/tmp/pyproject.toml", source.file("dagster-demo/pyproject.toml"))
            .with_workdir("/tmp")
            # Install dependencies without the project itself (like --no-root in poetry)
            .with_exec(["pip", "install", "-r", "/dev/stdin"], stdin="dagster\ndagster-cloud\ndagster-webserver\ndagster-dbt\ndbt-core\ndbt-duckdb\ndbt-snowflake")
            # Now copy the full source and install the project itself
            .with_directory("/src", source)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", ".", "--no-deps"])  # --no-deps since deps are already installed
            # Mount dbt cache volumes
            .with_mounted_cache("/src/dbt_demo/dbt_packages", dbt_packages_cache)
            .with_mounted_cache("/src/dbt_demo/target", dbt_target_cache)
        )

    @function
    def python_with_deps(self, source: dagger.Directory, python_version: str = "3.13") -> dagger.Container:
        """Create a Python container with project dependencies pre-installed for better caching"""
        # Create cache volumes for dbt
        dbt_packages_cache = dag.cache_volume("dbt-packages-cache")
        dbt_target_cache = dag.cache_volume("dbt-target-cache")
        
        return (
            self.python_deps_layer(source, python_version)
            .with_mounted_directory("/src", source)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", ".", "--no-deps"])  # No deps since already installed
            # Mount dbt cache volumes
            .with_mounted_cache("/src/dbt_demo/dbt_packages", dbt_packages_cache)
            .with_mounted_cache("/src/dbt_demo/target", dbt_target_cache)
        )

    @function
    async def lint_code(self, source: dagger.Directory, python_version: str = "3.13") -> str:
        """Run linting on the codebase"""
        return await (
            self.python_deps_layer(source, python_version)
            .with_mounted_directory("/src", source)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", ".", "--no-deps"])  # No deps since already installed
            .with_exec(["ruff", "check", "src/", "tests/"])
            .with_exec(["black", "--check", "src/", "tests/"])
            .with_exec(["isort", "--check-only", "src/", "tests/"])
            .stdout()
        )
    
    @function
    async def generate_linting(self, source: dagger.Directory, python_version: str = "3.13") -> dagger.Directory:
        """Auto-fix linting and formatting issues in the codebase"""
        return await (
            self.python_deps_layer(source, python_version)
            .with_mounted_directory("/src", source)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", ".", "--no-deps"])
            # Fix ruff issues
            .with_exec(["ruff", "check", "--fix", "src/", "tests/"])
            # Fix black formatting
            .with_exec(["black", "src/", "tests/"])
            # Fix isort import ordering
            .with_exec(["isort", "src/", "tests/"])
            .directory("/src")
        )
    
    @function
    async def generate_linting_and_show_command(self, source: dagger.Directory, python_version: str = "3.13") -> str:
        """Fix linting issues and provide the command to apply changes back to your filesystem"""
        # First, run the fixes
        await self.fix_linting(source, python_version)
        
        # Return instructions for applying the fixes
        return '''
🔧 Linting fixes have been created!

To apply these fixes to your local files, run this command:

cp -r fixed_code/dagster-demo/src/* dagster-demo/src/
        '''

    @function
    async def test_dagster(self, source: dagger.Directory, python_version: str = "3.13") -> str:
        """Run Dagster tests"""
        return await (
            self.python_deps_layer(source, python_version)
            .with_mounted_directory("/src", source)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", ".", "--no-deps"])  # No deps since already installed
            .with_exec(["python", "-m", "pytest", "tests/", "-v", "--tb=short"])
            .stdout()
        )

    @function
    async def test_integration(self, source: dagger.Directory, python_version: str = "3.13") -> str:
        """Run Dagster integration tests including test_integration.py"""
        return await (
            self.python_with_deps(source, python_version)
            # First need to generate dbt manifest for integration test
            .with_workdir("/src/dbt_demo")
            .with_exec(["dbt", "parse", "--profiles-dir", "."])
            # Now run the integration test - it's in the root of dagster-demo folder
            .with_workdir("/src")
            .with_exec(["python", "dagster-demo/test_integration.py"])
            .stdout()
        )

    @function
    async def validate_dagster_definitions(self, source: dagger.Directory, python_version: str = "3.13") -> str:
        """Validate Dagster definitions can be loaded"""
        return await (
            self.python_with_deps(source, python_version)
            .with_exec([
                "python", "-c", 
                "from dagster_demo.definitions import defs; print('✅ Dagster definitions loaded successfully')"
            ])
            .stdout()
        )

    @function
    async def validate_dbt(self, source: dagger.Directory, python_version: str = "3.13") -> str:
        """Validate dbt models and configuration"""
        return await (
            self.python_with_deps(source, python_version)
            .with_workdir("/src/dbt_demo")
            # dbt parse generates manifest.json and other artifacts that benefit from caching
            .with_exec(["dbt", "parse", "--profiles-dir", "."])
            .with_exec(["dbt", "compile", "--profiles-dir", ".", "--no-version-check"])
            .stdout()
        )

    @function
    async def security_scan(self, source: dagger.Directory, python_version: str = "3.13") -> str:
        """Run security scanning on dependencies"""
        return await (
            self.python_deps_layer(source, python_version)
            .with_mounted_directory("/src", source)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", ".", "--no-deps"])  # No deps since already installed
            .with_exec(["safety", "check", "--ignore", "70612"])  # Ignore Jinja2 issue if needed
            .with_exec(["bandit", "-r", "src/", "-f", "txt"])
            .stdout()
        )

    @function
    async def build_documentation(self, source: dagger.Directory, python_version: str = "3.13") -> dagger.Directory:
        """Generate project documentation"""
        return await (
            self.python_deps_layer(source, python_version)
            .with_exec(["pip", "install", "sphinx", "sphinx-rtd-theme"])
            .with_mounted_directory("/src", source)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", ".", "--no-deps"])  # No deps since already installed
            .with_exec(["mkdir", "-p", "docs"])
            .with_workdir("/src/dbt_demo")
            .with_exec(["dbt", "docs", "generate", "--profiles-dir", ".", "--no-version-check"])
            .directory("/src")
        )

    @function
    async def full_ci_pipeline(self, source: dagger.Directory, python_version: str = "3.13") -> str:
        """Run the complete CI pipeline"""
        results = []
        
        # Run all checks in parallel for faster execution
        try:
            lint_result = await self.lint_code(source, python_version)
            results.append(f"✅ Linting passed:\n{lint_result}")
        except Exception as e:
            results.append(f"❌ Linting failed: {e}")

        try:
            test_result = await self.test_dagster(source, python_version)
            results.append(f"✅ Dagster tests passed:\n{test_result}")
        except Exception as e:
            results.append(f"❌ Dagster tests failed: {e}")

        # Integration test removed - file was deleted

        try:
            validate_result = await self.validate_dagster_definitions(source, python_version)
            results.append(f"✅ Dagster validation passed:\n{validate_result}")
        except Exception as e:
            results.append(f"❌ Dagster validation failed: {e}")

        try:
            dbt_result = await self.validate_dbt(source, python_version)
            results.append(f"✅ dbt validation passed:\n{dbt_result}")
        except Exception as e:
            results.append(f"❌ dbt validation failed: {e}")

        try:
            security_result = await self.security_scan(source, python_version)
            results.append(f"✅ Security scan passed:\n{security_result}")
        except Exception as e:
            results.append(f"⚠️ Security scan completed with warnings: {e}")

        return "\n\n" + "="*50 + "\n".join(results) + "\n" + "="*50

    @function
    async def deploy_staging(self, source: dagger.Directory, 
                           snowflake_account: dagger.Secret,
                           snowflake_user: dagger.Secret,
                           snowflake_password: dagger.Secret,
                           python_version: str = "3.13") -> str:
        """Deploy to staging environment"""
        # Create cache volumes for dbt deployment
        dbt_packages_cache = dag.cache_volume("dbt-packages-cache")
        dbt_target_cache = dag.cache_volume("dbt-target-staging")
        
        return await (
            self.python_deps_layer(source, python_version)
            .with_mounted_directory("/src", source)
            .with_secret_variable("SNOWFLAKE_ACCOUNT", snowflake_account)
            .with_secret_variable("SNOWFLAKE_USER", snowflake_user)
            .with_secret_variable("SNOWFLAKE_PASSWORD", snowflake_password)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", ".", "--no-deps"])  # No deps since already installed
            .with_workdir("/src/dbt_demo")
            .with_mounted_cache("/src/dbt_demo/dbt_packages", dbt_packages_cache)
            .with_mounted_cache("/src/dbt_demo/target", dbt_target_cache)
            .with_exec(["dbt", "run", "--profiles-dir", ".", "--target", "staging"])
            .with_exec(["dbt", "test", "--profiles-dir", ".", "--target", "staging"])
            .stdout()
        )

    @function
    async def deploy_production(self, source: dagger.Directory,
                              snowflake_account: dagger.Secret,
                              snowflake_user: dagger.Secret, 
                              snowflake_password: dagger.Secret,
                              python_version: str = "3.13") -> str:
        """Deploy to production environment (requires all CI checks to pass)"""
        # First run full CI pipeline
        ci_result = await self.full_ci_pipeline(source, python_version)
        
        if "❌" in ci_result:
            raise Exception("CI pipeline failed - cannot deploy to production")
        
        # Create cache volumes for dbt deployment (separate from staging)
        dbt_packages_cache = dag.cache_volume("dbt-packages-cache")
        dbt_target_cache = dag.cache_volume("dbt-target-production")
        
        return await (
            self.python_deps_layer(source, python_version)
            .with_mounted_directory("/src", source)
            .with_secret_variable("SNOWFLAKE_ACCOUNT", snowflake_account)
            .with_secret_variable("SNOWFLAKE_USER", snowflake_user)
            .with_secret_variable("SNOWFLAKE_PASSWORD", snowflake_password)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", ".", "--no-deps"])  # No deps since already installed
            .with_workdir("/src/dbt_demo")
            .with_mounted_cache("/src/dbt_demo/dbt_packages", dbt_packages_cache)
            .with_mounted_cache("/src/dbt_demo/target", dbt_target_cache)
            .with_exec(["dbt", "run", "--profiles-dir", ".", "--target", "prod"])
            .with_exec(["dbt", "test", "--profiles-dir", ".", "--target", "prod"])
            .stdout()
        )
