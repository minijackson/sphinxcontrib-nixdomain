from __future__ import annotations

import re
from enum import StrEnum


class EntityType(StrEnum):
    OPTION = "Nix option"
    FUNCTION = "Nix function"


def option_key_fun(path: str) -> str:
    """Key function to path to sorted() for sorting options."""
    # Make sure ".enable" are sorted first
    if path.endswith(".enable"):
        # Note the "." is missing here,
        # to avoid sorting e.g. ".settings.enable" before ".settings"
        return path.removesuffix("enable")
    return path


def option_lt(left: str, right: str) -> bool:
    """Compare two options signature, sorting ".enable" first."""
    return sorted([left, right], key=option_key_fun)[0] == left


IDENTIFIER = r"(?:[a-zA-Z_][a-zA-Z0-9_'-]*)"
STR = r'(?:"(?:[^"\\]|\\.)*")'
ATTRIBUTE = re.compile(f"{STR}|{IDENTIFIER}", re.ASCII)


def split_attr_path(path: str) -> list[str]:
    return re.findall(ATTRIBUTE, path)
