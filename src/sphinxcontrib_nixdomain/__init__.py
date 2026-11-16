"""A Sphinx extension providing domain & objects for documenting Nix code."""

from __future__ import annotations

import importlib.metadata
import os
from typing import TYPE_CHECKING

import sphinx.directives.admonitions
from sphinx.util import logging

from ._data import load_object_files
from ._domain import NixDomain

if TYPE_CHECKING:
    from docutils import nodes
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.util.typing import ExtensionMetadata


logger = logging.getLogger(__name__)


def objects_json_files_from_env(_config: Config) -> list[str]:
    """Get the list of object files from the {env}`NIXDOMAIN_OBJECTS` env var."""
    if object_files := os.environ.get("NIXDOMAIN_OBJECTS"):
        return object_files.split(":")

    logger.warning(
        "nixdomain: No $NIXDOMAIN_OBJECTS file specified, "
        "no Nix object will be documented.",
    )
    return []


def _default_offline(_config: Config) -> bool:
    return bool(os.environ.get("NIX_BUILD_TOP") and not os.environ.get("IN_NIX_SHELL"))


def _config_messages(_app: Sphinx, config: Config):
    if not config.nixdomain_offline:
        logger.info("nixdomain: disabling online features.")


class Example(sphinx.directives.admonitions.Admonition):
    required_arguments = 0

    def run(self) -> list[nodes]:
        self.arguments.append("Example")
        return super().run()


def setup(app: Sphinx) -> ExtensionMetadata:
    """Set up the Nix Sphinx domain."""
    app.add_domain(NixDomain)
    app.add_config_value(
        "nixdomain_objects",
        objects_json_files_from_env,
        "html",
        list[str],
    )
    # Not "html" here, because we'd get a warning about the function being unpickable
    app.add_config_value("nixdomain_linkcode_resolve", None, "")
    app.add_config_value("nixdomain_offline", _default_offline, "html", bool)
    app.add_config_value("nixdomain_default_channel", "nixos-unstable", "html", str)

    app.connect("config-inited", load_object_files)
    app.connect("config-inited", _config_messages)

    app.add_directive(".caution", sphinx.directives.admonitions.Caution)
    app.add_directive(".important", sphinx.directives.admonitions.Important)
    app.add_directive(".note", sphinx.directives.admonitions.Note)
    app.add_directive(".tip", sphinx.directives.admonitions.Tip)
    app.add_directive(".warning", sphinx.directives.admonitions.Warning)
    app.add_directive(".example", Example)

    return {
        "version": importlib.metadata.version("sphinxcontrib-nixdomain"),
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
