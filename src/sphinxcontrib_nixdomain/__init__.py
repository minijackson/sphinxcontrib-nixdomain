"""A Sphinx extension providing domain & objects for documenting Nix code."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._domain import NixDomain

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata


# TODO: add options to the future autodoc:
# - flat: choose whether the options are displayed flat or nested
# - show_prefix: if options are displayed nested,
#   choose whether the option prefix is repeated

# TODO: add links to the source

object_data = tuple[str, str, str, str, str, int]


def setup(app: Sphinx) -> ExtensionMetadata:
    """Set up the Nix Sphinx domain."""
    app.add_domain(NixDomain)
    app.add_config_value("nix_options_json_files", [], "html", list[str])

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
