import pathlib

from pyrannic.support.importing import import_modules


def test_import_modules():
    """Test the import_modules function."""

    root = pathlib.Path().resolve()
    path = str(pathlib.Path(__file__).parent.resolve()).replace(str(root), "")
    path = f"{path.lstrip('/')}/package_test"

    modules = list(import_modules(path))

    assert len(modules) > 0, "No modules were imported."

    for module_path, module in modules:
        assert module.__name__ == module_path
        assert module_path.split(".")[-1] in ["foo_module", "bar_module", "baz_module"]
