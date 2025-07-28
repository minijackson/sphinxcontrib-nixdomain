"""Handle a set of packages."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, cast

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.util.docfields import Field, TypedField

from ._utils import split_attr_path

if TYPE_CHECKING:
    from collections.abc import Callable

    from sphinx.addnodes import desc_signature
    from sphinx.directives import ObjDescT

    from . import NixDomain


class PackageDirective(ObjectDescription):
    """Describe a package."""

    has_content = True
    required_arguments = 1
    option_spec: ClassVar[dict[str, Callable[[str], Any]]] = {
        "no-index": directives.flag,
        "no-index-entry": directives.flag,
        "no-contents-entry": directives.flag,
        "no-typesetting": directives.flag,
        "short-toc-name": directives.flag,
        "declaration": directives.unchanged,
    }

    doc_field_types: list[Field] = [
        TypedField(
            "override",
            label="Overrides",
            names=("override", "overrides"),
            can_collapse=True,
        ),
    ]

    def handle_signature(self, sig: str, signode: desc_signature) -> str:
        """Print the option given its signature."""
        no_index = "no-index" in self.options or "no-index-entry" in self.options

        signode["fullname"] = fullname = sig
        signode["path-parts"] = sig_names = split_attr_path(sig)
        signode["name"] = sig_names[-1]

        if not no_index:
            signode += addnodes.index(
                entries=[
                    (
                        "single",
                        sig,
                        _package_target(fullname),
                        "",
                        None,
                    ),
                ],
            )

        for el in sig_names[:-1]:
            signode += addnodes.desc_addname(text=el)
            signode += addnodes.desc_sig_punctuation(text=".")

        signode += addnodes.desc_name(text=sig_names[-1])

        declaration = self.options.get("declaration")

        if declaration and self.config.nix_linkcode_resolve is not None:
            uri = self.config.nix_linkcode_resolve(declaration)

            # Mostly taken from the 'linkcode' builtin extension
            onlynode = addnodes.only(expr="html")
            onlynode += nodes.reference(
                "",
                "",
                nodes.inline("", "[source]", classes=["viewcode-link"]),
                internal=False,
                refuri=uri,
            )
            signode += onlynode

        signode["short-toc-name"] = "short-toc-name" in self.options

        return sig

    def add_target_and_index(
        self,
        _name_cls: ObjDescT,
        _sig: str,
        signode: desc_signature,
    ) -> None:
        """Add the given option to the index, and create a target."""
        signode["ids"].append(_package_target(signode["fullname"]))

        nix = cast("NixDomain", self.env.get_domain("nix"))
        nix.add_package(signode["fullname"], {})

    def _object_hierarchy_parts(self, signode: desc_signature) -> tuple[str]:
        return tuple(signode["path-parts"])

    def _toc_entry_name(self, signode: desc_signature) -> str:
        if not signode.get("_toc_parts"):
            return ""

        if signode["short-toc-name"]:
            return signode["name"]

        return signode["fullname"]


def _package_target(fullname: str) -> str:
    """Return a target for referencing a option."""
    return f"nix-package-{fullname}"
