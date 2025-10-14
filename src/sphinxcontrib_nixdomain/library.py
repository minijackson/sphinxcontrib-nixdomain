"""Handle a Nix library API, such as functions."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any, ClassVar, cast

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Index, IndexEntry
from sphinx.util.docfields import Field, GroupedField, TypedField

from ._utils import split_attr_path

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from sphinx.addnodes import desc_signature
    from sphinx.directives import ObjDescT

    from . import NixDomain


class FunctionDirective(ObjectDescription):
    """Describe a function."""

    has_content = True
    required_arguments = 1
    option_spec: ClassVar[dict[str, Callable[[str], Any]]] = {
        "no-index": directives.flag,
        "no-index-entry": directives.flag,
        "no-contents-entry": directives.flag,
        "no-typesetting": directives.flag,
        "declaration": directives.unchanged,
    }

    doc_field_types: list[Field] = [  # noqa: RUF012
        # Mostly taken from the Python domain
        TypedField(
            "parameter",
            label="Parameters",
            names=(
                "param",
                "parameter",
                "arg",
                "argument",
                "keyword",
                "kwarg",
                "kwparam",
            ),
            typenames=("paramtype", "type"),
            can_collapse=True,
        ),
        Field(
            "returnvalue",
            label="Returns",
            has_arg=False,
            names=("returns", "return"),
        ),
        Field(
            "returntype",
            label="Return type",
            has_arg=False,
            names=("rtype",),
        ),
    ]

    def handle_signature(self, sig: str, signode: desc_signature) -> str:
        """Print the function given its signature."""
        signode["fullname"] = fullname = sig
        signode["path-parts"] = sig_names = split_attr_path(sig)
        signode["name"] = sig_names[-1]

        for el in sig_names[:-1]:
            signode += addnodes.desc_addname(text=el)
            signode += addnodes.desc_sig_punctuation(text=".")

        signode += addnodes.desc_name(text=sig_names[-1])

        declaration = self.options.get("declaration")

        if declaration and self.config.nixdomain_linkcode_resolve is not None:
            uri = self.config.nixdomain_linkcode_resolve(declaration)

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

        return fullname

    def add_target_and_index(
        self,
        fullname: str,
        _sig: str,
        signode: desc_signature,
    ) -> None:
        """Add the given function to the index, and create a target."""
        signode["ids"].append(_function_target(fullname))

        nix = cast("NixDomain", self.env.get_domain("nix"))
        nix.add_function(fullname, {})

        if "no-index-entry" not in self.options:
            self.indexnode["entries"].append(
                (
                    "single",
                    f"{fullname} (Nix function)",
                    _function_target(fullname),
                    "",
                    None,
                ),
            )

    def before_content(self) -> None:
        """Insert content before a function.

        In this instance, we insert ourself in the context
        so that we can refer to functions in the same scope.
        """
        scope = self.env.ref_context.setdefault("nix:function", [])
        scope.append(self.names[-1])

    def after_content(self) -> None:
        """Insert content after a option.

        In this instance, we remove our scope from the context.
        """
        scope = self.env.ref_context.setdefault("nix:function", [])
        if scope:
            scope.pop()
        else:
            self.env.ref_context.pop("nix:function")

    def _object_hierarchy_parts(self, signode: desc_signature) -> tuple[str]:
        return tuple(signode["path-parts"])

    def _toc_entry_name(self, signode: desc_signature) -> str:
        if not signode.get("_toc_parts"):
            return ""

        return signode["fullname"]


def _function_target(fullname: str) -> str:
    """Return a target for referencing a function."""
    return f"nix-function-{fullname}"


class LibraryIndex(Index):
    """Index over an API library."""

    # TODO: register as a page in order to be able to include the index in a toctree

    name = "libindex"
    localname = "Nix Library Index"
    shortname = "library"

    def generate(
        self,
        _docnames: Iterable[str] | None = None,
    ) -> tuple[list[tuple[str, list[IndexEntry]]], bool]:
        """Get entries for the index."""
        content: defaultdict[str, list[IndexEntry]] = defaultdict(list)

        nix = cast("NixDomain", self.domain)

        functions = list(nix.get_functions())
        functions = sorted(functions)

        for function in functions:
            entries = content.setdefault(function.path[0].lower(), [])
            # No need to handle nesting,
            # Sphinx currently support only one level of nesting,
            # which would be weird with Nix module options
            entries.append(
                # name, subtype, docname, anchor, extra, qualifier, description
                IndexEntry(
                    function.path,
                    0,
                    function.docname,
                    function.anchor,
                    function.docname,
                    "",
                    function.typ,
                ),
            )

        # convert the dict to the sorted list of tuples expected
        content_ = sorted(content.items())

        return content_, True
