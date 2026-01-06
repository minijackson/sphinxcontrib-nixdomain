from __future__ import annotations

import os.path
import re
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


class EntityType(StrEnum):
    OPTION = "option"
    FUNCTION = "function"
    PACKAGE = "package"

    def directive_name(self) -> str:
        return str(self)

    def human_name(self) -> str:
        match self:
            case EntityType.OPTION:
                return "Nix option"
            case EntityType.FUNCTION:
                return "Nix function"
            case EntityType.PACKAGE:
                return "Nix package"


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


IDENTIFIER = r"(?:<?[a-zA-Z_][a-zA-Z0-9_'-]*>?)"
STR = r'(?:"(?:[^"\\]|\\.)*")'
ATTRIBUTE = re.compile(f"{STR}|{IDENTIFIER}", re.ASCII)


def split_attr_path(path: str) -> list[str]:
    return re.findall(ATTRIBUTE, path)


def is_part_of_scope(scope_loc: list[str], loc: list[str], *, recursive: bool) -> bool:
    if not recursive and len(loc) != len(scope_loc) + 1:
        return False

    return loc[: len(scope_loc)] == scope_loc


def skipped_options_levels(
    previous_loc: list[str],
    next_loc: list[str],
) -> Generator[str]:
    """Return all skipped options level.

    For example, if documenting 'a.b.c' then 'a.d.e.f',
    it yields ['a.d', 'a.d.e'].

    If no levels were skipped, it yields nothing.
    """
    common_prefix_len = len(os.path.commonprefix([previous_loc, next_loc]))
    next_loc_len = len(next_loc)

    if next_loc_len - common_prefix_len <= 1:
        return

    for i in range(common_prefix_len + 1, next_loc_len):
        yield ".".join(next_loc[:i])
