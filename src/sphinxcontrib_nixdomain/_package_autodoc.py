from collections.abc import Callable
from copy import copy
from pathlib import Path
from typing import Any, ClassVar

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import StringList, string2lines
from jinja2.sandbox import SandboxedEnvironment
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.util.template import SphinxTemplateLoader

from . import _data as autodata
from ._utils import is_part_of_scope, split_attr_path
from .package import PackageDirective

logger = logging.getLogger(__name__)


class NixAutoPackageDirective(SphinxDirective):
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

        package = autodata.get_package(name)
        if package is None:
            logger.warning(
                "Could not find option '%s' in any of the 'nixdomain_objects' files",
                name,
                location=self.get_location(),
            )
            return []

        builtin_templates_path = Path(__file__).parent / "templates"

        template_loader = SphinxTemplateLoader(
            self.env.srcdir,
            self.config.templates_path,
            [builtin_templates_path],
        )

        env = SandboxedEnvironment(
            loader=template_loader,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        template = env.get_template("nixdomain/package.md.jinja")
        content = template.render({"pkg": package, "name": name})

        directive_options: dict[str, Any] = copy(self.options)
        if package.meta.position is not None:
            directive_options["declaration"] = package.meta.position

        return PackageDirective(
            "nix:package",
            arguments=[name],
            options=directive_options,
            content=StringList(
                string2lines(
                    content,
                    self.state.document.settings.tab_width,
                    convert_whitespace=True,
                ),
                # TODO: use declarations
                source="<Nix package>",
            ),
            lineno=self.lineno,
            content_offset=self.content_offset,
            block_text=self.block_text,
            state=self.state,
            state_machine=self.state_machine,
        ).run()


class NixAutoPackagesDirective(SphinxDirective):
    has_content = False
    required_arguments = 0
    optional_arguments = 1
    option_spec: ClassVar[dict[str, Callable[[str], Any]]] = {
        "no-index": directives.flag,
        "no-index-entry": directives.flag,
        "no-contents-entry": directives.flag,
        "no-typesetting": directives.flag,
        "no-recursive": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        scope = self.arguments[0] if len(self.arguments) >= 1 else ""
        scope_loc = split_attr_path(scope)

        # If "no-recursive" is given, `self.options["no-recursive"]` is `None`,
        # so its bool representation is `False`.
        #
        # We pop it to pass the rest of the options to the `autopackage` directive.
        recursive = bool(self.options.pop("no-recursive", True))

        pkgs = [
            name
            for name, pkg in autodata.packages()
            if is_part_of_scope(scope_loc, pkg.loc, recursive=recursive)
        ]

        if pkgs == []:
            logger.warning(
                "No package found for scope: '%s'",
                scope,
                location=self.get_location(),
            )
            return []

        result: list[nodes.Node] = []

        for pkg in pkgs:
            result += NixAutoPackageDirective(
                "nix:autopackage",
                arguments=[pkg],
                options=self.options,
                content=StringList(),
                lineno=self.lineno,
                content_offset=self.content_offset,
                block_text=self.block_text,
                state=self.state,
                state_machine=self.state_machine,
            ).run()

        return result
