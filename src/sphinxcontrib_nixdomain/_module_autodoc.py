"""Implementation of the various autodoc directive for the Nix domain."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from docutils.statemachine import StringList, string2lines
from sphinx.directives import code
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from .module import ModuleOptionDirective

if TYPE_CHECKING:
    from ._domain import NixDomain


logger = logging.getLogger(__name__)

# TODO: internal, visible, read_only, related_packages, configurable links to source

class NixAutoOptionDirective(SphinxDirective):
    has_content = False
    required_arguments = 1

    def run(self) -> list[nodes.Node]:
        nix: NixDomain = self.env.get_domain("nix")

        name = self.arguments[0]

        if name not in nix.auto_options_doc:
            logger.warning(
                "Could not find option '%s' in any of the 'nix_options_json_files'",
                name,
            )
            return []

        option = nix.auto_options_doc[name]

        description = None
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

        directive_options = {}
        if option.typ is not None:
            directive_options["type"] = option.typ

        rendered = ModuleOptionDirective(
            "nix:module-opt",
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

        if option.declarations != []:
            declaration_nodes = [nodes.term("Declared in", "Declared in")]
            for decl in option.declarations:
                decl_para = nodes.paragraph("", decl)
                declaration_nodes += [nodes.definition("", decl_para)]

            declarations = nodes.definition_list_item("", *declaration_nodes)
            rendered_content += nodes.definition_list("", declarations)

        return rendered


class NixAutoModuleDirective(SphinxDirective):
    pass
