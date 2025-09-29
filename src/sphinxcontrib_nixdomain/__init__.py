"""A Sphinx extension providing domain & objects for documenting Nix code."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from sphinx.util import logging

from ._data import load_object_files
from ._domain import NixDomain

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.util.typing import ExtensionMetadata


logger = logging.getLogger(__name__)


def objects_json_files_from_env(_config: Config) -> list[str]:
    """Get the list of object files from the {env}`NIXDOMAIN_OBJECTS` env var."""
    if object_files := os.environ.get("NIXDOMAIN_OBJECTS"):
        return object_files.split(":")

    logger.warning(
        "No $NIXDOMAIN_OBJECTS file specified, no Nix object will be documented.",
    )
    return []


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
    app.add_config_value("nixdomain_toc_display_full_path", True, "html", bool)  # noqa: FBT003

    app.connect("config-inited", load_object_files)

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
