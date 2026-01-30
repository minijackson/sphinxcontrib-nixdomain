# Roles

:::{tip}
With Intersphinx,
these cross-references can resolve to objects
defined in an external Sphinx project.
See {doc}`../usage/cross-references`
for more information.
:::

:::{rst:role} nix:obj
Refer to any object defined by `sphinxcontrib-nixdomain`.

For example:

``` markdown
See the {nix:obj}`services.autobar.enable` object.
```

Is rendered as:

> See the {nix:obj}`services.autobar.enable` object.
:::

:::{rst:role} nix:option
Refer to an option from the NixOS module system.

For example:

``` markdown
See the {nix:option}`services.autobar.enable` option.
```

Is rendered as:

> See the {nix:option}`services.autobar.enable` option.
:::

:::{rst:role} nix:pkg
Refer to a Nix package.

For example:

``` markdown
See the {nix:pkg}`hello` package.
```

Is rendered as:

> See the {nix:pkg}`hello` package.
:::

:::{rst:role} nix:func
Refer to a Nix function.

For example:

``` markdown
See the {nix:func}`exampleLib.myFunc` function.
```

Is rendered as:

> See the {nix:func}`exampleLib.myFunc` function.
:::
