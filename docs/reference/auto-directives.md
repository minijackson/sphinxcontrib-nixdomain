# Automatic directives

## Options

Sphinx directives for automatically documenting NixOS options,
or any option in a NixOS-like module system.

:::{rst:directive} .. nix:automodule:: <module>

Render all options documentation in the module `module`, recursively.

For an example usage, see the <project:#module-example> example.
:::

:::{rst:directive} .. nix:autooption:: <option>

Render documentation for the single `option`.

For an example usage, see the <project:#option-example> example.
:::

## Packages

Sphinx directives for automatically documenting Nix packages.

:::{rst:directive} .. nix:autopackages:: [scope]

Render all packages documentation in the scope `scope`, recursively.
If no `scope` is given, render all found packages.

For an example usage, see the <project:#packages-example> example.
:::

:::{rst:directive} .. nix:autopackage:: <package>

Render documentation for the single `package`.

For an example usage, see the <project:#package-example> example.
:::

## Library

Sphinx directives for automatically documenting a library of Nix functions.

:::{rst:directive} .. nix:autolibrary:: [scope]

Render all functions documentation in the scope `scope`, recursively.
If no `scope` is given, render all found functions.

For an example usage, see the <project:#library-example> example.
:::

:::{rst:directive} .. nix:autofunction:: <function>

Render documentation for the single `function`.

For an example usage, see the <project:#function-example> example.
:::
