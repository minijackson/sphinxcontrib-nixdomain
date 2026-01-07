# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from datetime import date
from urllib.parse import urlsplit

from sphinx.util import logging

sys.path.append(os.path.abspath("../src"))  # noqa: PTH100

logger = logging.getLogger(__name__)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "sphinxcontrib-nixdomain"
author = "Minijackson"
release = "0.1.0"

source_repository = "https://github.com/minijackson/sphinxcontrib-nixdomain"

source_date = date.today()
if date_ts := os.environ.get("SOURCE_DATE_EPOCH"):
    source_date = date.fromtimestamp(float(date_ts))

today = source_date.isoformat()
copyright = f"2023-{source_date.year}, Minijackson"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinxcontrib_nixdomain",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinx_design",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# primary_domain = "nix"

intersphinx_mapping = {
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "myst": ("https://myst-parser.readthedocs.io/en/latest/", None),
    "epnix": ("https://epics-extensions.github.io/EPNix/dev/", None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ["_static"]
html_baseurl = "https://minijackson.github.io/sphinxcontrib-nixdomain/"


html_css_files = ["field-lists.css"]

html_theme = "furo"
html_theme_options = {
    "source_repository": source_repository,
    "source_branch": "main",
    "source_directory": "docs/",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/minijackson/sphinxcontrib-nixdomain",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}

# -- Options for the Nix domain ----------------------------------------------

revision = os.environ.get("REVISION", "main")


def nixdomain_linkcode_resolve(path: str) -> str:
    url = urlsplit(path)

    fragment = "#" + url.fragment if url.fragment else ""

    match url.netloc:
        case "self":
            return f"{source_repository}/blob/{revision}{url.path}{fragment}"
        case "nixpkgs":
            return f"https://github.com/NixOS/nixpkgs/blob/master{url.path}{fragment}"

    logger.warning("no source repository for url: %s", path)
    return ""


# -- Options for the MyST parser ---------------------------------------------
# https://myst-parser.readthedocs.io/en/latest/configuration.html

myst_enable_extensions = ["colon_fence", "fieldlist"]

myst_url_schemes = {
    "http": None,
    "https": None,
    "mailto": None,
    "source": {
        "url": f"{source_repository}/blob/{revision}/{{{{path}}}}",
        "title": "{{path}}",
        "classes": ["github"],
    },
}
