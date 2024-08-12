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
from .library import FunctionDirective, LibraryIndex
from .module import ModuleOptionDirective, ModuleOptionIndex

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

class NixDomain(Domain):
    name = "nix"
    label = "Nix"
    roles = {  # noqa: RUF012
        "bind": XRefRole(),
        # TODO:
        # "func": XRefRole(),
        "modopt": XRefRole(),
        "ref": XRefRole(),
    }
    directives = {  # noqa: RUF012
        "automodule": NixAutoModuleDirective,
        "autooption": NixAutoOptionDirective,
        "function": FunctionDirective,
        "module-opt": ModuleOptionDirective,
    }
    indices = [  # noqa: RUF012
        LibraryIndex,
        ModuleOptionIndex,
    ]
    initial_data = {  # noqa: RUF012
        "bindings": [],
        "module-opts": [],
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

    def get_bindings(self) -> Generator[object_data]:
        """Get all bindings in this domain."""
        yield from self.data["bindings"]

    def get_module_options(self) -> Generator[object_data]:
        """Get all module options in this domain."""
        yield from self.data["module-opts"]

    def get_objects(self) -> Generator[object_data]:
        """Get all objects in this domain."""
        yield from self.get_bindings()
        yield from self.get_module_options()

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
        elif typ == "modopt":
            object_getter = self.get_module_options
        elif typ == "ref":
            object_getter = self.get_objects
        else:
            logger.warning("Unknown Nix object type: %s", typ)
            return None

        match = [
            (docname, anchor)
            for name, sig, typ, docname, anchor, prio in object_getter()
            if sig == target
        ]

        if len(match) > 0:
            todocname = match[0][0]
            targ = match[0][1]
            return make_refnode(builder, fromdocname, todocname, targ, contnode, targ)

        logger.warning(
            "No reference found for Nix object type: %s, with target: %s",
            typ,
            target,
            location=fromdocname,
        )
        return None

    def add_binding(self, path: str, typ: str, _arguments: dict[str, str]) -> None:
        """Add a new binding to the domain."""
        name = f"nix.function.{path}"
        anchor = f"nix-function-{path}"

        self.data["bindings"].append(
            (name, path, typ, self.env.docname, anchor, 0),
        )

    def add_module_option(self, signature: str, _options: dict[str, str]) -> None:
        """Add a new module option to the domain."""
        name = f"nix.module-opt.{signature}"
        anchor = f"nix-module-opt-{signature}"

        # name, dispname, type, docname, anchor, priority
        self.data["module-opts"].append(
            (name, signature, "Module option", self.env.docname, anchor, 0),
        )
