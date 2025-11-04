"""Test version consistency across different files."""

import re
from pathlib import Path

import revbits


def get_version_from_init() -> str:
    """Get version from __init__.py."""
    version: str = revbits.__version__
    return version


def get_version_from_pyproject() -> str:
    """Get version from pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    content = pyproject_path.read_text(encoding="utf-8")

    # Find version in pyproject.toml
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if match is None:
        msg = "Could not find version in pyproject.toml"
        raise ValueError(msg)

    return match.group(1)


def test_version_consistency() -> None:
    """Test that version in __init__.py matches version in pyproject.toml."""
    init_version = get_version_from_init()
    pyproject_version = get_version_from_pyproject()

    assert init_version == pyproject_version, (
        f"Version mismatch: __init__.py has {init_version}, " f"but pyproject.toml has {pyproject_version}"
    )


def test_version_format() -> None:
    """Test that version follows semantic versioning format."""
    version = get_version_from_init()

    # Check semantic versioning format (MAJOR.MINOR.PATCH or MAJOR.MINOR.PATCH-prerelease)
    pattern = r"^\d+\.\d+\.\d+(?:-[a-zA-Z0-9.]+)?$"
    assert re.match(pattern, version), f"Version {version} does not follow semantic versioning format"
