# Manual directives

You can declare Nix objects manually
by using the following directives.

Use these directives when generating from Nix code isn't possible
or if you want to develop a custom documentation generator.

:::{seealso}
{doc}`../tests/manual` for more manual usage examples.
:::

::::::{rst:directive} .. nix:option:: name
Describes a option from the NixOS module system.

For example:

``` markdown
:::{nix:option} service.my-service.enable
My option description
:::
```

Is rendered as:

> :::{nix:option} service.my-service.enable
> :no-index:
>
> My option description
> :::

:::{rubric} Options
:::

:::{rst:directive:option} type
:type: text

The option type,
for example ``list of string``.
:::

:::{rst:directive:option} read-only
Add this option of the option is read-only.
:::

:::{rst:directive:option} declaration
:type: text

A link to the source code.
See the {confval}`nixdomain_linkcode_resolve` configuration
to generate a ``[source]`` link.
:::

Other standard domain options are supported,
see the Sphinx domain {ref}`Basic Markup <basic-domain-markup>` documentation.
::::::

::::::{rst:directive} .. nix:package:: name
Describes a Nix package.

Use {ref}`field-lists <rst-field-lists>` after the description
to describe the package's metadata

For example:

``` markdown
:::{nix:package} myProject.myPackage
My package description

:version: `0.0.0-rc1`
:license: `EUPL-1.2`
:::
```

Will be rendered as:

> :::{nix:package} myProject.myPackage
> :no-index:
>
> My package description
>
> :version: `0.0.0-rc1`
> :license: `EUPL-1.2`
> :::

:::{rubric} Options
:::

:::{rst:directive:option} declaration
:type: text

A link to the source code.
See the {confval}`nixdomain_linkcode_resolve` configuration
to generate a ``[source]`` link.
:::

Other standard domain options are supported,
see the Sphinx domain {ref}`Basic Markup <basic-domain-markup>` documentation.
::::::

::::::{rst:directive} .. nix:function:: name
Describes a Nix function.

Use {ref}`field-lists <rst-field-lists>` after the description
to describe function parameter, their types, the return value, etc.

For example:

``` markdown
:::{nix:function} lib.myFunction
My function description

:param int a: a number
:param int b: another number
:returns: the sum of those two numbers
:rtype: int
:::
```

Will be rendered as:

> :::{nix:function} lib.myFunction
> :no-index:
>
> My function description
>
> :param int a: a number
> :param int b: another number
> :returns: the sum of those two numbers
> :rtype: int
> :::

:::{rubric} Options
:::

:::{rst:directive:option} declaration
:type: text

A link to the source code.
See the {confval}`nixdomain_linkcode_resolve` configuration
to generate a ``[source]`` link.
:::

Other standard domain options are supported,
see the Sphinx domain {ref}`Basic Markup <basic-domain-markup>` documentation.
::::::
