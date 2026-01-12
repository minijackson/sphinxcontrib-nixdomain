# Cross-references

## Cross-referencing Nix objects

To cross-reference Nix objects,
you can use these {external+sphinx:term}`Sphinx roles <role>`:

- {rst:role}`nix:option`
- {rst:role}`nix:pkg`
- {rst:role}`nix:func`

:::{seealso}
For a complete list of roles,
see the {doc}`../reference/roles` reference.
:::

For example,
in Markdown:

``` markdown
See the {nix:option}`services.autobar.package` option,
which is {nix:pkg}`hello` by default.

You might also want to examine {nix:func}`exampleLib.myFunc`.
```

Is rendered as:

> See the {nix:option}`services.autobar.package` option,
> which is {nix:pkg}`hello` by default.
>
> You might also want to examine {nix:func}`exampleLib.myFunc`.

## Cross-referencing external Nix objects

You can also reference Nix objects from any external documentation
that uses Sphinx and `sphinxcontrib-nixdomain`,
by using the {external+sphinx:ref}`Intersphinx <ext-intersphinx>` built-in Sphinx extension.

:::{important}
This feature requires an internet connection.
This means that you have to build your documentation outside of the Nix sandbox,
as this is intentionally not reproducible.
:::

Add the project you want to link to
in the {confval}`intersphinx_mapping` configuration:

```{code-block} python
:caption: {file}`conf.py` --- Adding the external documentation to Intersphinx

intersphinx_mapping = {
    "nixdomain": ("https://sphinxcontrib-nixdomain.readthedocs.io/en/stable/", None),
    # Another example project using `sphinxcontrib-nixdomain`
    "epnix": ("https://epics-extensions.github.io/EPNix/dev/", None),
}
```

With this configuration,
any cross-referenced object might resolve
to these external documentation.

For example:

``` markdown
See the {nix:func}`nixdomainLib.documentObjects`
and the {nix:pkg}`epnix.epics-base` package.
```

Renders:

> See the {nix:func}`nixdomainLib.documentObjects`
> and the {nix:pkg}`epnix.epics-base` package.

### Explicit target

To explicitly select which project to link,
use the {samp}`\{external+{project}:{role}\}` syntax.
For example:

``` markdown
See the {external+epnix:nix:option}`programs.phoebus-client.enable` option.
```

Renders:

> See the {external+epnix:nix:option}`programs.phoebus-client.enable` option.

### Turning off automatic resolve

To turn off automatically resolving to an external project,
set the {confval}`intersphinx_disabled_reftypes` option.
