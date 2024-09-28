"""Handle a set of NixOS-like module options."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any, Callable, ClassVar, cast

from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Index, IndexEntry

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sphinx.addnodes import desc_signature
    from sphinx.directives import ObjDescT

    from . import NixDomain

# TODO: make a class for Module / ModuleOption


class OptionDirective(ObjectDescription):
    """Describe an option.

    Should be used for NixOS-like modules.
    """

    has_content = True
    required_arguments = 1
    option_spec: ClassVar[dict[str, Callable[[str], Any]]] = {
        "noindex": directives.flag,
        "type": directives.unchanged,
    }

    def handle_signature(self, sig: str, signode: desc_signature) -> str:
        """Print the option given its signature."""
        signode["noindex"] = noindex = "noindex" in self.options

        parent_opts = self.env.ref_context.setdefault("nix:option", [])
        signode["fullname"] = fullname = ".".join([*parent_opts, sig])

        sig_names = sig.split(".")

        if not noindex:
            signode += addnodes.index(
                entries=[
                    (
                        "single",
                        fullname,
                        _option_target(signode["fullname"]),
                        "",
                        None,
                    ),
                ],
            )

        for el in sig_names[:-1]:
            signode += addnodes.desc_addname(text=el)
            signode += addnodes.desc_sig_punctuation(text=".")

        signode += addnodes.desc_name(text=sig_names[-1])

        ftype = self.options.get("type")

        signode["type"] = ftype

        if ftype:
            signode += addnodes.desc_type(text=f" {ftype}")

        return sig

    def add_target_and_index(
        self,
        _name_cls: ObjDescT,
        _sig: str,
        signode: desc_signature,
    ) -> None:
        """Add the given option to the index, and create a target."""
        signode["ids"].append(_option_target(signode["fullname"]))

        nix = cast("NixDomain", self.env.get_domain("nix"))
        nix.add_option(signode["fullname"], {})

    def before_content(self) -> None:
        """Insert content before a option.

        In this instance, we insert ourself in the context
        so that our children can see us as parent.
        """
        options = self.env.ref_context.setdefault("nix:option", [])
        options.append(self.names[-1])

    def after_content(self) -> None:
        """Insert content after a option.

        In this instance, we remove ourself in the context
        to prevent other options to see us as parent.
        """
        options = self.env.ref_context.setdefault("nix:option", [])
        if options:
            options.pop()
        else:
            self.env.ref_context.pop("nix:option")

    def _object_hierarchy_parts(self, signode: desc_signature) -> tuple[str]:
        return tuple(signode["fullname"].split("."))

    def _toc_entry_name(self, signode: desc_signature) -> str:
        if not signode.get("_toc_parts"):
            return ""

        return signode["fullname"]


def _option_target(fullname: str) -> str:
    """Return a target for referencing a option."""
    return f"nix-option-{fullname}"


class OptionsIndex(Index):
    """Index over options."""

    name = "optionsindex"
    localname = "Nix options index"
    shortname = "option"

    def generate(
        self,
        _docnames: Iterable[str] | None = None,
    ) -> tuple[list[tuple[str, list[IndexEntry]]], bool]:
        """Get entries for the index."""
        content: defaultdict[str, list[IndexEntry]] = defaultdict(list)

        nix = cast("NixDomain", self.domain)

        # sort the list of recipes in alphabetical order
        options = list(nix.get_options())
        options = sorted(options, key=lambda option: option.signature)

        # generate the expected output, shown below, from the above using the
        # first letter of the recipe as a key to group thing
        #
        # TODO: use the "top" module as key?
        for _name, dispname, typ, docname, anchor, _priority in options:
            entries = content.setdefault(dispname[0].lower(), [])
            # No need to handle nesting,
            # Sphinx currently support only one level of nesting,
            # which would be weird with Nix module options
            entries.append(
                # name, subtype, docname, anchor, extra, qualifier, description
                IndexEntry(dispname, 0, docname, anchor, docname, "", typ),
            )

        # convert the dict to the sorted list of tuples expected
        content_ = sorted(content.items())

        return content_, True
