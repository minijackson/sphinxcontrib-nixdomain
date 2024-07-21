from __future__ import annotations

from typing import TYPE_CHECKING

from sphinx.domains import Domain
from sphinx.roles import XRefRole
from sphinx.util.nodes import make_refnode

from .library import FunctionDirective, LibraryIndex
from .module import ModuleOptionDirective, ModuleOptionIndex

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

# TODO: add options to the future autodoc:
# - flat: choose whether the options are displayed flat or nested
# - show_prefix: if options are displayed nested,
#   choose whether the option prefix is repeated

# TODO: add links to the source


class NixDomain(Domain):
    name = "nix"
    label = "Nix"
    roles = {
        "bind": XRefRole(),
        # TODO:
        # "func": XRefRole(),
        "modopt": XRefRole(),
        "ref": XRefRole(),
    }
    directives = {
        "module-opt": ModuleOptionDirective,
        "function": FunctionDirective,
    }
    indices = [
        LibraryIndex,
        ModuleOptionIndex,
    ]
    initial_data = {
        "bindings": [],
        "module-opts": [],
    }
    data_version = 0

    def get_full_qualified_name(self, node):
        return f"nix.{node.arguments[0]}"

    def get_bindings(self):
        yield from self.data["bindings"]

    def get_module_options(self):
        yield from self.data["module-opts"]

    def get_objects(self):
        yield from self.get_bindings()
        yield from self.get_module_options()

    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        object_getter = None
        if typ == "bind":
            object_getter = self.get_bindings
        elif typ == "modopt":
            object_getter = self.get_module_options
        elif typ == "ref":
            object_getter = self.get_objects

        match = [
            (docname, anchor)
            for name, sig, typ, docname, anchor, prio in object_getter()
            if sig == target
        ]

        if len(match) > 0:
            todocname = match[0][0]
            targ = match[0][1]
            return make_refnode(builder, fromdocname, todocname, targ, contnode, targ)
        else:
            # TODO: print a proper warning?
            print(f"Awww, found nothing for {target} and type {typ}")
            return None

    def add_binding(self, path: str, typ: str, arguments):
        """Add a new binding to the domain."""
        name = f"nix.function.{path}"
        anchor = f"nix-function-{path}"

        self.data["bindings"].append(
            (name, path, typ, self.env.docname, anchor, 0),
        )

    def add_module_option(self, signature: str, options):
        """Add a new module option to the domain."""
        name = f"nix.module-opt.{signature}"
        anchor = f"nix-module-opt-{signature}"

        # name, dispname, type, docname, anchor, priority
        self.data["module-opts"].append(
            (name, signature, "Module option", self.env.docname, anchor, 0),
        )


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_domain(NixDomain)

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
