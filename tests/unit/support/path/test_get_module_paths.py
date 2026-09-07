import os

from pyrannic.support.path import get_module_paths


def test_get_module_paths():
    """Test the get_module_paths function with various inputs."""

    file_path = os.path.abspath(os.path.dirname(__file__))
    test_path = os.path.join(file_path, "test_folder")

    test_files = [
        "20260831_0000_foo.py",
        "20260831_0001_baz.py",
        "20260907_0000_foo.py",
        "20260907_0001_bar.py",
        "20260907_0002_baz.py",
    ]

    files = get_module_paths(test_path)

    for index, file in enumerate(files):
        assert os.path.basename(file) == test_files[index]
