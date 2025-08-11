from pathlib import Path

from dagster import definitions, load_from_defs_folder


@definitions
def defs():
    # Point to the project root directory (where pyproject.toml is located)
    project_root = Path(__file__).parent.parent.parent
    return load_from_defs_folder(project_root=project_root)
