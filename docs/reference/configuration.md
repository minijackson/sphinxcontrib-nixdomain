# Configuration

```{role} code-py(code)
:language: Python
```

::::::{confval} nixdomain_linkcode_resolve
:type: {code-py}`Callable[[str], str] | None`
:default: {code-py}`None`

A function that maps a `:declaration:` to a URL.

If set,
this uses the {py:mod}`sphinx.ext.linkcode` mechanism to
add a ``[source]`` link next to documented objects.

Takes a special URL as argument,
in the form {samp}`{source}:{path}`
with an optional {samp}`#L{n}` fragment.

_source_ is the resolved source repository name,
and corresponds to one of the `sources` argument
of {nix:func}`nixdomainLib.documentObjects`.

_path_ is the path to the file declaring the object,
relative to the _source_.

:::{rubric} Example
:::

```{code-block} python
:caption: {file}`conf.py` --- set {code-py}`nixdomain_linkcode_resolve`

from urllib.parse import urlsplit

from sphinx.util import logging

logger = logging.getLogger(__name__)

# [Rest of the configuration...]

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
```
::::::
