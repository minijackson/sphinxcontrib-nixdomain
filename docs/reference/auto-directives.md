# Automatic directives

## Options

Sphinx directives for automatically documenting NixOS options,
or any option in a NixOS-like module system.

::::::{rst:directive} .. nix:automodule:: [module]

Render all options documentation in the module `module`, recursively.
If no `module` is given,
render all modules.

For an example usage, see the <project:#module-example> example.

:::{rubric} Options
:::

:::{rst:directive:option} no-recursive
If given,
generate the documentation
of options directly under the given module,
without recursing into sub-modules.
:::
::::::

:::{rst:directive} .. nix:autooption:: <option>

Render documentation for the single `option`.

For an example usage, see the <project:#option-example> example.
:::

## Packages

Sphinx directives for automatically documenting Nix packages.

::::::{rst:directive} .. nix:autopackages:: [scope]

Render all packages documentation in the scope `scope`, recursively.
If no `scope` is given,
render all packages
found in the top-level scope.

For an example usage, see the <project:#packages-example> example.

:::{rubric} Options
:::

:::{rst:directive:option} no-recursive
If given,
generate the documentation
of packages directly under the given scope,
without recursing into sub-scopes.
:::
::::::

:::{rst:directive} .. nix:autopackage:: <package>

Render documentation for the single `package`.

For an example usage, see the <project:#package-example> example.
:::

## Library

Sphinx directives for automatically documenting a library of Nix functions.

::::::{rst:directive} .. nix:autolibrary:: [scope]

Render all functions documentation in the scope `scope`, recursively.
If no `scope` is given,
render all functions
found in the top-level scope.

For an example usage, see the <project:#library-example> example.

:::{rubric} Options
:::

:::{rst:directive:option} no-recursive
If given,
generate the documentation
of functions directly under the given scope,
without recursing into sub-scopes.
:::
::::::

:::{rst:directive} .. nix:autofunction:: <function>

Render documentation for the single `function`.

For an example usage, see the <project:#function-example> example.
:::
