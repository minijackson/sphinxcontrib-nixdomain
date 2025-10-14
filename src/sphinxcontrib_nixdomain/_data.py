from collections.abc import Iterable
from pathlib import Path
from typing import Annotated, Any

from pydantic import BaseModel as PydanticBaseModel
from pydantic import BeforeValidator, ConfigDict, Field, model_validator
from sphinx._cli.util.colour import bold
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util import logging

from ._utils import split_attr_path

logger = logging.getLogger(__name__)


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(frozen=True)


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


class PackageLicense(BaseModel):
    full_name: str = Field(alias="fullName")
    url: str | None = None


def _normalize_license(value: Any) -> PackageLicense:
    if isinstance(value, str):
        return PackageLicense(fullName=value)

    return PackageLicense(**value)


def _normalize_licenses(value: Any) -> list[PackageLicense]:
    if isinstance(value, list):
        return [_normalize_license(l) for l in value]

    return [_normalize_license(value)]


# From nixpkgs/lib/tests/maintainer-module.nix
class PackageMaintainer(BaseModel):
    name: str
    email: str | None = None
    matrix: str | None = None
    github: str | None = None


class PackageMeta(BaseModel):
    description: str = ""
    long_description: str = Field(alias="longDescription", default="")

    homepage: str | None = None
    download_page: str | None = Field(alias="downloadPage", default=None)
    changelog: str | None = None

    broken: bool = False
    insecure: bool = False
    unfree: bool = False

    licenses: Annotated[
        list[PackageLicense],
        BeforeValidator(_normalize_licenses),
        Field(alias="license", default=[]),
    ]
    maintainers: list[PackageMaintainer] = []

    position: str | None = None


class Package(BaseModel):
    name: str
    loc: list[str]
    version: str | None
    meta: PackageMeta


class Function(BaseModel):
    name: str
    loc: list[str]
    description: str
    location: str | None

    @model_validator(mode="before")
    @classmethod
    def _set_loc(cls, data: Any) -> Any:
        if isinstance(data, dict):
            data["loc"] = split_attr_path(data["name"])
        return data


class Objects(BaseModel):
    options: dict[str, Option] = {}
    packages: dict[str, Package] = {}
    library: dict[str, Function] = {}


_OBJECTS: Objects


def load_object_files(_app: Sphinx, config: Config) -> None:
    for file in config.nixdomain_objects:
        logger.info(bold("loading Nix objects in %s... "), file, nonl=True)
        global _OBJECTS
        _OBJECTS = Objects.model_validate_json(Path(file).read_text())
        logger.info(
            "loaded %s options, %s packages, and %s functions",
            len(_OBJECTS.options),
            len(_OBJECTS.packages),
            len(_OBJECTS.library),
        )


def get_option(name: str) -> Option | None:
    return _OBJECTS.options.get(name)


def has_option(name: str) -> bool:
    return name in _OBJECTS.options


def options() -> Iterable[tuple[str, Option]]:
    return _OBJECTS.options.items()


def get_package(name: str) -> Package | None:
    return _OBJECTS.packages.get(name)


def packages() -> Iterable[tuple[str, Package]]:
    return _OBJECTS.packages.items()


def get_function(name: str) -> Function | None:
    return _OBJECTS.library.get(name)


def functions() -> Iterable[tuple[str, Function]]:
    return _OBJECTS.library.items()
