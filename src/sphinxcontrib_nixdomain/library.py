from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, ClassVar

from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Index, IndexEntry


class FunctionDirective(ObjectDescription):
    """Describe a function."""

    has_content = True
    required_arguments = 1
    option_spec: ClassVar[dict[str, Callable[[str], Any]]] = {
        "type": directives.unchanged,
    }

    def handle_signature(self, sig: str, signode: addnodes.desc_signature):
        # TODO: attribute path to the function
        signode["fullname"] = sig

        # parent_opts = self.env.ref_context.setdefault("nix:module-opt", [])
        # signode["fullname"] = ".".join(parent_opts + [sig])

        # TODO: arguments
        # TODO: return type

        signode += addnodes.desc_name(text=sig)

        return sig

    def add_target_and_index(self, name_cls, sig, signode):
        signode["ids"].append(f"nix-function-" + signode["fullname"])

        nix = self.env.get_domain("nix")
        nix.add_binding(signode["fullname"], "Function", {})

    # def before_content(self) -> None:
    #     module_opts = self.env.ref_context.setdefault("nix:module-opt", [])
    #     module_opts.append(self.names[-1])
    #
    # def after_content(self) -> None:
    #     module_opts = self.env.ref_context.setdefault("nix:module-opt", [])
    #     if module_opts:
    #         module_opts.pop()
    #     else:
    #         self.env.ref_context.pop("nix:module-opt")

    def _object_hierarchy_parts(self, signode: addnodes.desc_signature) -> tuple[str]:
        return tuple(signode["fullname"].split("."))

    def _toc_entry_name(self, signode: addnodes.desc_signature) -> str:
        if not signode.get("_toc_parts"):
            return ""

        return signode["fullname"]


class LibraryIndex(Index):
    """Index over an API library."""

    name = "libindex"
    localname = "Nix Library Index"
    shortname = "library"

    def generate(self, docnames=None):
        content = defaultdict(list)

        # sort the list of recipes in alphabetical order
        bindings = self.domain.get_bindings()
        bindings = sorted(bindings, key=lambda binding: binding[0])

        # generate the expected output, shown below, from the above using the
        # first letter of the recipe as a key to group thing
        #
        # TODO: use the attribute path as key?
        for _name, dispname, typ, docname, anchor, _priority in bindings:
            entries = content.setdefault(dispname[0].lower(), [])
            # No need to handle nesting,
            # Sphinx currently support only one level of nesting,
            # which would be weird with Nix module options
            entries.append(
                # name, subtype, docname, anchor, extra, qualifier, description
                IndexEntry(dispname, 0, docname, anchor, docname, "", typ),
            )

        # convert the dict to the sorted list of tuples expected
        content = sorted(content.items())

        return content, True
