# sphinxcontrib-nixdomain

:::{warning}
This library is under active development
and doesn't have a stable release yet.
:::

`sphinxcontrib-nixdomain` is a {external+sphinx:doc}`Sphinx <index>` extension
providing a {external+sphinx:term}`Sphinx domain <domain>` for Nix.

The goal of this project is to be able to document
NixOS module options,
Nix packages,
Nix libraries,
using the Sphinx documentation ecosystem.

:::{important}
`sphinxcontrib-nixdomain` assumes you're writing your Sphinx documentation
in Markdown with the {external+myst:doc}`MyST extension <index>`.

Examples in this documentation are in Markdown.
:::

```{toctree}
:caption: Usage:
:hidden:

usage/quick-start
usage/cross-references
```

```{toctree}
:caption: Examples:
:hidden:

examples/auto-options
examples/auto-packages
examples/auto-library
```

```{toctree}
:caption: Reference:
:hidden:

reference/configuration
reference/auto-directives
reference/roles
reference/nix-library
reference/manual
reference/changelog
```

```{toctree}
:caption: Tests:
:hidden:

tests/manual
```

# Indices and tables

* {ref}`genindex`
* {ref}`nix-optionsindex`
* {ref}`nix-libindex`
