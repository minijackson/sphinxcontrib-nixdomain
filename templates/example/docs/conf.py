# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from urllib.parse import urlsplit

from sphinx.util import logging

logger = logging.getLogger(__name__)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "my-project"
copyright = "%Y, me"
author = "me"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinxcontrib_nixdomain",
    "sphinx_design",
    "myst_parser",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for the MyST parser ---------------------------------------------
# https://myst-parser.readthedocs.io/en/latest/configuration.html

# These syntax extensions are required by `sphinxcontrib-nixdomain`
myst_enable_extensions = ["colon_fence", "fieldlist"]

# -- Options for the Nix domain ----------------------------------------------
# https://minijackson.github.io/sphinxcontrib-nixdomain/reference/configuration.html


def nixdomain_linkcode_resolve(path: str) -> str:
    url = urlsplit(path)

    fragment = "#" + url.fragment if url.fragment else ""

    match url.netloc:
        case "self":
            return f"https://example.com/blob/master{url.path}{fragment}"
        case "nixpkgs":
            return f"https://github.com/NixOS/nixpkgs/blob/master{url.path}{fragment}"

    logger.warning("no source repository for url: %s", path)
    return ""
