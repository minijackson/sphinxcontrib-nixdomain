from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, ClassVar

from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Index, IndexEntry

# TODO: make a class for Module / ModuleOption

class ModuleOptionDirective(ObjectDescription):
    """Describe a module option.

    Should be used for NixOS-like modules.
    """

    has_content = True
    required_arguments = 1
    option_spec: ClassVar[dict[str, Callable[[str], Any]]] = {
        "type": directives.unchanged,
    }

    def handle_signature(self, sig: str, signode: addnodes.desc_signature):
        parent_opts = self.env.ref_context.setdefault("nix:module-opt", [])
        signode["fullname"] = ".".join(parent_opts + [sig])

        sig_names = sig.split(".")

        for el in sig_names[:-1]:
            signode += addnodes.desc_addname(text=el)
            signode += addnodes.desc_sig_punctuation(text=".")

        signode += addnodes.desc_name(text=sig_names[-1])

        ftype = self.options.get("type")

        signode["type"] = ftype

        if ftype:
            signode += addnodes.desc_type(text=f" {ftype}")

        return sig

    def add_target_and_index(self, name_cls, sig, signode):
        signode["ids"].append(f"nix-module-opt-" + signode["fullname"])
        nix = self.env.get_domain("nix")

        nix.add_module_option(signode["fullname"], {"type": self.options.get("type")})

    def before_content(self) -> None:
        module_opts = self.env.ref_context.setdefault("nix:module-opt", [])
        module_opts.append(self.names[-1])

    def after_content(self) -> None:
        module_opts = self.env.ref_context.setdefault("nix:module-opt", [])
        if module_opts:
            module_opts.pop()
        else:
            self.env.ref_context.pop("nix:module-opt")

    def _toc_entry_name(self, signode: addnodes.desc_signature) -> str:
        return signode["fullname"]


class ModuleOptionIndex(Index):
    """Index over module options."""

    name = "modoptindex"
    localname = "Nix Module Option Index"
    shortname = "module-opt"

    def generate(self, docnames=None):
        content = defaultdict(list)

        # sort the list of recipes in alphabetical order
        module_opts = self.domain.get_module_options()
        module_opts = sorted(module_opts, key=lambda module_opt: module_opt[0])

        # generate the expected output, shown below, from the above using the
        # first letter of the recipe as a key to group thing
        #
        # TODO: use the "top" module as key?
        for _name, dispname, typ, docname, anchor, _priority in module_opts:
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

