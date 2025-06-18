from __future__ import annotations

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
from ._utils import EntityType, option_lt, split_attr_path
from .library import FunctionDirective, LibraryIndex
from .module import OptionDirective, OptionsIndex
from .package import PackageDirective

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


class NixXRefRole(XRefRole):
    def process_link(
        self,
        env: BuildEnvironment,
        refnode: Element,
        has_explicit_title: bool,
        title: str,
        target: str,
    ) -> tuple[str, str]:
        refnode["nix:option"] = env.ref_context.get("nix:option", [""])[-1]
        return super().process_link(env, refnode, has_explicit_title, title, target)


class NixDomain(Domain):
    name = "nix"
    label = "Nix"
    roles = {  # noqa: RUF012
        "bind": NixXRefRole(),
        # TODO:
        # "func": XRefRole(),
        "option": NixXRefRole(),
        "pkg": NixXRefRole(),
        "ref": NixXRefRole(),
    }
    directives = {  # noqa: RUF012
        "automodule": NixAutoModuleDirective,
        "autooption": NixAutoOptionDirective,
        "function": FunctionDirective,
        "option": OptionDirective,
        "package": PackageDirective,
    }
    indices = [  # noqa: RUF012
        LibraryIndex,
        OptionsIndex,
    ]
    initial_data = {  # noqa: RUF012
        "bindings": [],
        "options": [],
        "packages": [],
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

    def get_packages(self) -> Generator[RefEntity]:
        """Get all options in this domain."""
        yield from self.data["packages"]

    def get_entities(self) -> Generator[RefEntity]:
        """Get all entities in this domain."""
        yield from self.get_options()
        yield from self.get_packages()
        yield from self.get_bindings()

    def get_objects(self) -> Generator[object_data]:
        """Get all entities in this domain.

        Returns a tuple, as needed by Sphinx.
        """
        for entity in self.get_entities():
            yield entity.to_tuple()

    def resolve_xref(
        self,
        _env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        typ: str,
        target: str,
        node: pending_xref,
        contnode: Element,
    ) -> Element | None:
        """Resolve the pending_xref node with the given typ and target."""
        object_getter = None
        if typ == "bind":
            context_path = []
            object_getter = self.get_bindings
        elif typ == "option":
            context_path = split_attr_path(node.get("nix:option", ""))
            object_getter = self.get_options
        elif typ == "pkg":
            context_path = split_attr_path(node.get("nix:package", ""))
            object_getter = self.get_packages
        elif typ == "ref":
            context_path = []
            object_getter = self.get_entities
        else:
            logger.warning("Unknown Nix object type: %s", typ)
            return None

        target_path = split_attr_path(target)

        # Make a list of possible referred attributes,
        # depending on the context
        candidates = [
            ".".join(context_path[:prefix_len] + target_path)
            for prefix_len in range(len(context_path) + 1)
        ]
        # Order candidates by most nested attribute first
        candidates.reverse()

        matches = [entity for entity in object_getter() if entity.path in candidates]
        # Sort matches according to the candidates list
        matches.sort(key=lambda entity: candidates.index(entity.path))

        if len(matches) > 0:
            entity = matches[0]
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

    def add_binding(
        self,
        path: str,
        typ: EntityType,
        _arguments: dict[str, str],
    ) -> None:
        """Add a new binding to the domain."""
        name = f"nix.function.{path}"
        anchor = f"nix-function-{path}"

        self.data["bindings"].append(
            RefEntity(name, path, typ, self.env.docname, anchor, 0),
        )

    def add_option(self, path: str, _options: dict[str, str]) -> None:
        """Add a new module option to the domain."""
        name = f"nix.option.{path}"
        anchor = f"nix-option-{path}"

        self.data["options"].append(
            RefEntity(name, path, EntityType.OPTION, self.env.docname, anchor, 0),
        )

    def add_package(self, path: str, _options: dict[str, str]) -> None:
        """Add a new module option to the domain."""
        name = f"nix.package.{path}"
        anchor = f"nix-package-{path}"

        self.data["packages"].append(
            RefEntity(name, path, EntityType.PACKAGE, self.env.docname, anchor, 0),
        )
