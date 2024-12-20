"""Implementation of the various autodoc directive for the Nix domain."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, ClassVar, cast

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import StringList, string2lines
from sphinx.directives import code
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from ._utils import option_key_fun, skipped_options_levels, split_attr_path
from .module import OptionDirective

if TYPE_CHECKING:
    from typing import Any

    from ._domain import AutoOptionDoc, NixDomain


logger = logging.getLogger(__name__)

# TODO: internal, visible, read_only, related_packages, configurable links to source


class NixAutoOptionDirective(SphinxDirective):
    has_content = False
    required_arguments = 1
    option_spec: ClassVar[dict[str, Callable[[str], Any]]] = {
        "short-toc-name": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        nix = cast("NixDomain", self.env.get_domain("nix"))

        name = self.arguments[0]

        short_toc_name = "short-toc-name" in self.options

        if name not in nix.auto_options_doc:
            logger.warning(
                "Could not find option '%s' in any of the 'nix_options_json_files'",
                name,
            )
            return []

        option = nix.auto_options_doc[name]

        description = StringList()
        if option.description is not None:
            description = StringList(
                string2lines(
                    option.description,
                    self.state.document.settings.tab_width,
                    convert_whitespace=True,
                ),
                # TODO: use declarations
                source="<NixOS-like option>",
            )

        directive_options: dict[str, Any] = {}
        if option.typ is not None:
            directive_options["type"] = option.typ

        if option.read_only:
            directive_options["read-only"] = True

        if short_toc_name:
            directive_options["short-toc-name"] = True

        if option.declarations != []:
            # Not sure how to handle multiple declarations
            directive_options["declaration"] = option.declarations[0]

        rendered = OptionDirective(
            "nix:option",
            arguments=[name],
            options=directive_options,
            content=description,
            lineno=self.lineno,
            content_offset=self.content_offset,
            block_text=self.block_text,
            state=self.state,
            state_machine=self.state_machine,
        ).run()

        rendered_content = rendered[-1][-1]

        if option.default is not None:
            # Not sure if container_wrapper is public or private API
            rendered_content += code.container_wrapper(
                self,
                nodes.literal_block(option.default, option.default, language="nix"),
                "Default value",
            )

        if option.example is not None:
            # Not sure if container_wrapper is public or private API
            rendered_content += code.container_wrapper(
                self,
                nodes.literal_block(option.example, option.example, language="nix"),
                "Example",
            )

        if option.declarations != [] and self.config.nix_linkcode_resolve is None:
            declaration_nodes: list[nodes.Element] = [
                nodes.term("Declared in", "Declared in"),
            ]
            for decl in option.declarations:
                decl_para = nodes.paragraph("", decl)
                declaration_nodes += [nodes.definition("", decl_para)]

            declarations = nodes.definition_list_item("", *declaration_nodes)
            rendered_content += nodes.definition_list("", declarations)

        return rendered


class NixAutoModuleDirective(SphinxDirective):
    has_content = False
    required_arguments = 1

    def run(self) -> list[nodes.Node]:
        nix = cast("NixDomain", self.env.get_domain("nix"))

        module = self.arguments[0]
        module_loc = split_attr_path(module)

        def _is_part_of_module(option: AutoOptionDoc) -> bool:
            return option.loc[: len(module_loc)] == module_loc

        options = [
            name
            for name, option in nix.auto_options_doc.items()
            if _is_part_of_module(option)
        ]

        if options == []:
            logger.warning("No options found for module: '%s'", module)
            return []

        short_toc_name = (
            {"short-toc-name": True}
            if not self.config.nix_toc_display_full_path
            else {}
        )

        result = []

        if module not in nix.auto_options_doc:
            result += OptionDirective(
                "nix:option",
                arguments=[module],
                options={},
                content=StringList(),
                lineno=self.lineno,
                content_offset=self.content_offset,
                block_text=self.block_text,
                state=self.state,
                state_machine=self.state_machine,
            ).run()

        previous_option_loc = module_loc

        for option in sorted(options, key=option_key_fun):
            option_loc = split_attr_path(option)

            for in_between_option in skipped_options_levels(
                previous_option_loc,
                option_loc,
            ):
                result += OptionDirective(
                    "nix:option",
                    arguments=[in_between_option],
                    options=short_toc_name,
                    content=StringList(),
                    lineno=self.lineno,
                    content_offset=self.content_offset,
                    block_text=self.block_text,
                    state=self.state,
                    state_machine=self.state_machine,
                ).run()

            result += NixAutoOptionDirective(
                "",
                arguments=[option],
                options=short_toc_name if option != module else {},
                content=StringList(),
                lineno=self.lineno,
                content_offset=self.content_offset,
                block_text=self.block_text,
                state=self.state,
                state_machine=self.state_machine,
            ).run()

            previous_option_loc = option_loc

        return result
