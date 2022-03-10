"""Tests for the hypothesmith package metadata."""
import re
from pathlib import Path
from typing import NamedTuple, Optional

import flake8_async


class Version(NamedTuple):
    year: int
    month: int
    day: int

    @classmethod
    def from_string(cls, string):
        return cls(*map(int, string.split(".")))


UNRELEASED_VERSION = Version(0, 0, 0)


def get_latest_release() -> Optional[Version]:
    valid_pattern = re.compile(r"^## (\d\d\.\d?\d\.\d?\d)$")
    unlreleased_pattern = re.compile(r"^## UNRELEASED$")
    with open(Path(__file__).parent.parent / "CHANGELOG.md") as f:
        for aline in f.readlines():
            version_match = valid_pattern.match(aline)
            if version_match:
                return Version.from_string(version_match.group(1))
            unlreleased_match = unlreleased_pattern.match(aline)
            if unlreleased_match:
                return UNRELEASED_VERSION

    return None


def test_last_release_against_changelog():
    """Ensure we have the latest version covered in CHANGELOG.md"""
    last_version = get_latest_release()
    if last_version != UNRELEASED_VERSION:
        assert last_version == Version.from_string(flake8_async.__version__)
