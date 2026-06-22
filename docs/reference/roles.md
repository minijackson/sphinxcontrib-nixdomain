# Roles

:::{tip}
With Intersphinx,
these cross-references can resolve to objects
defined in an external Sphinx project.
See {doc}`../usage/cross-references`
for more information.
:::

::::::{rst:role} nix:obj
Refer to any object defined by `sphinxcontrib-nixdomain`.

:::{admonition} Example
``` markdown
See the {nix:obj}`services.autobar.enable` object.
```

Renders:

> See the {nix:obj}`services.autobar.enable` object.
:::
::::::

::::::{rst:role} nix:option
Refer to an option from the NixOS module system.

:::{admonition} Example
``` markdown
See the {nix:option}`services.autobar.enable` option.
```

Renders:

> See the {nix:option}`services.autobar.enable` option.
:::
::::::

::::::{rst:role} nix:pkg
Refer to a Nix package.

:::{admonition} Example
``` markdown
See the {nix:pkg}`hello` package.
```

Renders:

> See the {nix:pkg}`hello` package.
:::
::::::

::::::{rst:role} nix:func
Refer to a Nix function.

:::{admonition} Example
``` markdown
See the {nix:func}`exampleLib.myFunc` function.
```

Renders:

> See the {nix:func}`exampleLib.myFunc` function.
:::
::::::
