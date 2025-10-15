"""Implementation of the various library autodoc directives for the Nix domain."""

from __future__ import annotations

from copy import copy
from typing import TYPE_CHECKING, Any, ClassVar

from docutils.parsers.rst import directives
from docutils.statemachine import StringList, string2lines
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from . import _data as autodata
from ._utils import split_attr_path
from .library import FunctionDirective

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

    from docutils import nodes

    from ._domain import NixDomain


logger = logging.getLogger(__name__)


class NixAutoFunctionDirective(SphinxDirective):
    has_content = False
    required_arguments = 1
    option_spec: ClassVar[dict[str, Callable[[str], Any]]] = {
        "no-index": directives.flag,
        "no-index-entry": directives.flag,
        "no-contents-entry": directives.flag,
        "no-typesetting": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        name = self.arguments[0]

        function = autodata.get_function(name)
        if function is None:
            logger.warning(
                "Could not find function '%s' in any of the 'nixdomain_objects' files",
                name,
                location=self.get_location(),
            )
            return []

        description = StringList()
        if function.description is not None:
            description = StringList(
                string2lines(
                    function.description,
                    self.state.document.settings.tab_width,
                    convert_whitespace=True,
                ),
                # TODO: use declarations
                source="<Nix function documentation>",
            )

        directive_options: dict[str, Any] = copy(self.options)
        if function.location is not None:
            directive_options["declaration"] = function.location

        return FunctionDirective(
            "nix:function",
            arguments=[name],
            options=directive_options,
            content=description,
            lineno=self.lineno,
            content_offset=self.content_offset,
            block_text=self.block_text,
            state=self.state,
            state_machine=self.state_machine,
        ).run()


class NixAutoLibraryDirective(SphinxDirective):
    has_content = False
    required_arguments = 0
    optional_arguments = 1
    option_spec: ClassVar[dict[str, Callable[[str], Any]]] = {
        "no-index": directives.flag,
        "no-index-entry": directives.flag,
        "no-contents-entry": directives.flag,
        "no-typesetting": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        scope = self.arguments[0] if len(self.arguments) >= 1 else ""
        scope_loc = split_attr_path(scope)

        def _is_part_of_scope(fun: autodata.Function) -> bool:
            return fun.loc[: len(scope_loc)] == scope_loc

        funcs = [name for name, pkg in autodata.functions() if _is_part_of_scope(pkg)]

        if funcs == []:
            logger.warning(
                "No function found for scope: '%s'",
                scope,
                location=self.get_location(),
            )
            return []

        result = []

        # TODO: sort?
        for fun in funcs:
            result += NixAutoFunctionDirective(
                "",
                arguments=[fun],
                options=self.options,
                content=StringList(),
                lineno=self.lineno,
                content_offset=self.content_offset,
                block_text=self.block_text,
                state=self.state,
                state_machine=self.state_machine,
            ).run()

        return result
