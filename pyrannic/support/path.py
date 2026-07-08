from glob import glob
from os import path


def get_module_paths(package_path: str) -> list[str]:
    """Returns a list of full paths of the modules in a given package."""

    pattern = "**/*.py"
    files = [f for f in glob(path.join(package_path, pattern), recursive=True)]

    return files
