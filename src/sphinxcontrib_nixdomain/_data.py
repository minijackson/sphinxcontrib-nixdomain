import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util import logging

logger = logging.getLogger(__name__)

class Option(BaseModel):
    name: str
    loc: list[str]
    typ: str | None
    description: str | None
    default: str | None
    example: str | None
    related_packages: str | None
    declarations: list[str]
    internal: bool
    visible: bool
    read_only: bool

class Objects(BaseModel):
    options: dict[str, Option] = {}

_OBJECTS: Objects


def load_object_files(_app: Sphinx, config: Config) -> None:
    for file in config.nixdomain_objects:
        logger.info("Loading Nix objects in %s", file)
        global _OBJECTS
        _OBJECTS = Objects.model_validate_json(Path(file).read_text())


def get_option(name: str) -> Option | None:
    return _OBJECTS.options.get(name)


def has_option(name: str) -> bool:
    return name in _OBJECTS.options


def options() -> Iterable[tuple[str, Option]]:
    return _OBJECTS.options.items()
