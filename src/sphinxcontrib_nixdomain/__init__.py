"""A Sphinx extension providing domain & objects for documenting Nix code."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._domain import NixDomain

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata


object_data = tuple[str, str, str, str, str, int]


def setup(app: Sphinx) -> ExtensionMetadata:
    """Set up the Nix Sphinx domain."""
    app.add_domain(NixDomain)
    app.add_config_value("nix_options_json_files", [], "html", list[str])
    # Not "html" here, because we'd get a warning about the function being unpickable
    app.add_config_value("nix_linkcode_resolve", None, "")
    app.add_config_value("nix_toc_display_full_path", True, "html", bool)  # noqa: FBT003

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
