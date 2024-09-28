from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Generator

from sphinx.domains import Domain
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.nodes import make_refnode

from ._module_autodoc import NixAutoModuleDirective, NixAutoOptionDirective
from ._utils import EntityType, option_lt
from .library import FunctionDirective, LibraryIndex
from .module import OptionDirective, OptionsIndex

if TYPE_CHECKING:
    from docutils.nodes import Element
    from sphinx.addnodes import pending_xref
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment


logger = logging.getLogger(__name__)

# TODO: add options to the future autodoc:
# - flat: choose whether the options are displayed flat or nested
# - show_prefix: if options are displayed nested,
#   choose whether the option prefix is repeated

# TODO: add links to the source

object_data = tuple[str, str, str, str, str, int]


@dataclass
class AutoOptionDoc:
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


AutoOptionsDoc = dict[str, AutoOptionDoc]


@dataclass
class RefEntity:
    """A referenceable Nix entity.

    This can be for example a binding (function, package) or an option.

    This dataclass is used to figure out the entity's info
    when a reference is resolved.
    """

    name: str
    path: str
    typ: EntityType
    docname: str
    anchor: str
    priority: int

    def to_tuple(self) -> tuple[str, str, str, str, str, int]:
        """Get this entity as tuple, as needed by Sphinx."""
        # name, dispname, type, docname, anchor, priority
        return (
            self.name,
            self.path,
            self.typ,
            self.docname,
            self.anchor,
            self.priority,
        )

    def __lt__(self, other: RefEntity) -> bool:
        if self.typ == EntityType.OPTION:
            # Sort .enable options first
            return option_lt(self.path, other.path)

        return self.path < other.path


class NixDomain(Domain):
    name = "nix"
    label = "Nix"
    roles = {  # noqa: RUF012
        "bind": XRefRole(),
        # TODO:
        # "func": XRefRole(),
        "option": XRefRole(),
        "ref": XRefRole(),
    }
    directives = {  # noqa: RUF012
        "automodule": NixAutoModuleDirective,
        "autooption": NixAutoOptionDirective,
        "function": FunctionDirective,
        "option": OptionDirective,
    }
    indices = [  # noqa: RUF012
        LibraryIndex,
        OptionsIndex,
    ]
    initial_data = {  # noqa: RUF012
        "bindings": [],
        "options": [],
    }
    data_version = 0

    @cached_property
    def auto_options_doc(self) -> AutoOptionsDoc:
        """Get the options documentation.

        As specified by the ``nix_options_json_files`` configuration.
        """
        result = {}
        for file in self.env.config.nix_options_json_files:
            logger.info("Loading options doc: %s", file)
            with Path(file).open() as f:
                content: dict[str, dict] = json.load(f)
                for k, v in content.items():
                    result[k] = AutoOptionDoc(**v)

        return result

    def get_bindings(self) -> Generator[RefEntity]:
        """Get all bindings in this domain."""
        yield from self.data["bindings"]

    def get_options(self) -> Generator[RefEntity]:
        """Get all options in this domain."""
        yield from self.data["options"]

    def get_entities(self) -> Generator[RefEntity]:
        """Get all entities in this domain."""
        yield from self.data["options"]

    def get_objects(self) -> Generator[object_data]:
        """Get all entities in this domain.

        Returns a tuple, as needed by Sphinx.
        """
        for entity in itertools.chain(self.get_options(), self.get_bindings()):
            yield entity.to_tuple()

    def resolve_xref(
        self,
        _env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        typ: str,
        target: str,
        _node: pending_xref,
        contnode: Element,
    ) -> Element | None:
        """Resolve the pending_xref node with the given typ and target."""
        object_getter = None
        if typ == "bind":
            object_getter = self.get_bindings
        elif typ == "option":
            object_getter = self.get_options
        elif typ == "ref":
            object_getter = self.get_entities
        else:
            logger.warning("Unknown Nix object type: %s", typ)
            return None

        match = [entity for entity in object_getter() if entity.path == target]

        if len(match) > 0:
            entity = match[0]
            return make_refnode(
                builder,
                fromdocname,
                entity.docname,
                entity.anchor,
                contnode,
                f"{entity.typ} {entity.path}",
            )

        logger.warning(
            "No reference found for Nix object type: %s, with target: %s",
            typ,
            target,
            location=fromdocname,
        )
        return None

    def add_binding(self, path: str, typ: EntityType, _arguments: dict[str, str]) -> None:
        """Add a new binding to the domain."""
        name = f"nix.function.{path}"
        anchor = f"nix-function-{path}"

        self.data["bindings"].append(
            RefEntity(name, path, typ, self.env.docname, anchor, 0)
        )

    def add_option(self, path: str, _options: dict[str, str]) -> None:
        """Add a new module option to the domain."""
        name = f"nix.option.{path}"
        anchor = f"nix-option-{path}"

        self.data["options"].append(
            RefEntity(name, path, EntityType.OPTION, self.env.docname, anchor, 0),
        )
