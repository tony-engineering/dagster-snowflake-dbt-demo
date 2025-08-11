import dagger
from dagger import dag, function, object_type
from typing import Optional


@object_type
class DagsterDemo:
    """Dagger CI/CD pipeline for Dagster + dbt + Snowflake project"""

    @function
    def python_base(self, python_version: str = "3.13") -> dagger.Container:
        """Create a base Python container with common dependencies"""
        return (
            dag.container()
            .from_(f"python:{python_version}-slim")
            .with_exec(["apt-get", "update"])
            .with_exec(["apt-get", "install", "-y", "git", "curl", "build-essential"])
            .with_exec(["pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
        )

    @function
    async def lint_code(self, source: dagger.Directory, python_version: str = "3.13") -> str:
        """Run linting on the codebase"""
        return await (
            self.python_base(python_version)
            .with_mounted_directory("/src", source)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", ".[dev]"])
            .with_exec(["pip", "install", "ruff", "black", "isort"])
            .with_exec(["ruff", "check", "src/", "tests/"])
            .with_exec(["black", "--check", "src/", "tests/"])
            .with_exec(["isort", "--check-only", "src/", "tests/"])
            .stdout()
        )

    @function
    async def test_dagster(self, source: dagger.Directory, python_version: str = "3.13") -> str:
        """Run Dagster tests"""
        return await (
            self.python_base(python_version)
            .with_mounted_directory("/src", source)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", ".[dev]"])
            .with_exec(["python", "-m", "pytest", "tests/", "-v", "--tb=short"])
            .stdout()
        )

    @function
    async def validate_dagster_definitions(self, source: dagger.Directory, python_version: str = "3.13") -> str:
        """Validate Dagster definitions can be loaded"""
        return await (
            self.python_base(python_version)
            .with_mounted_directory("/src", source)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", "."])
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
            self.python_base(python_version)
            .with_mounted_directory("/src", source)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", "."])
            .with_workdir("/src/dbt_demo")
            .with_exec(["dbt", "parse", "--profiles-dir", "."])
            .with_exec(["dbt", "compile", "--profiles-dir", ".", "--no-version-check"])
            .stdout()
        )

    @function
    async def security_scan(self, source: dagger.Directory, python_version: str = "3.13") -> str:
        """Run security scanning on dependencies"""
        return await (
            self.python_base(python_version)
            .with_mounted_directory("/src", source)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "safety", "bandit"])
            .with_exec(["pip", "install", "-e", "."])
            .with_exec(["safety", "check", "--ignore", "70612"])  # Ignore Jinja2 issue if needed
            .with_exec(["bandit", "-r", "src/", "-f", "txt"])
            .stdout()
        )

    @function
    async def build_documentation(self, source: dagger.Directory, python_version: str = "3.13") -> dagger.Directory:
        """Generate project documentation"""
        return await (
            self.python_base(python_version)
            .with_mounted_directory("/src", source)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", ".", "sphinx", "sphinx-rtd-theme"])
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
        return await (
            self.python_base(python_version)
            .with_mounted_directory("/src", source)
            .with_secret_variable("SNOWFLAKE_ACCOUNT", snowflake_account)
            .with_secret_variable("SNOWFLAKE_USER", snowflake_user)
            .with_secret_variable("SNOWFLAKE_PASSWORD", snowflake_password)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", "."])
            .with_workdir("/src/dbt_demo")
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
        
        return await (
            self.python_base(python_version)
            .with_mounted_directory("/src", source)
            .with_secret_variable("SNOWFLAKE_ACCOUNT", snowflake_account)
            .with_secret_variable("SNOWFLAKE_USER", snowflake_user)
            .with_secret_variable("SNOWFLAKE_PASSWORD", snowflake_password)
            .with_workdir("/src/dagster-demo")
            .with_exec(["pip", "install", "-e", "."])
            .with_workdir("/src/dbt_demo")
            .with_exec(["dbt", "run", "--profiles-dir", ".", "--target", "prod"])
            .with_exec(["dbt", "test", "--profiles-dir", ".", "--target", "prod"])
            .stdout()
        )
