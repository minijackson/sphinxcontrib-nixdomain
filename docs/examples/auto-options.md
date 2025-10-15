# Automatic NixOS-like options

```{default-domain} nix
```

:::{tip}
Click the `[source]` link next to the object
to open the declaration source file.

Click the eye icon in the upper-right of the page
to open the Markdown source file.
:::

(module-example)=
## Document a whole module

To document a whole module,
use the {rst:dir}`nix:automodule` directive.

For example:

``````markdown
```{default-domain} nix
```

```{automodule} services.autobar
```
``````

Renders:

> ```{automodule} services.autobar
> :no-contents-entry:
> :no-index-entry:
> ```

(option-example)=
## Document a single option

To document a single option,
use the {rst:dir}`nix:autooption` directive.

For example:

``````markdown
```{default-domain} nix
```

```{autooption} services.autobar.enable
```
``````

Renders:

> ```{autooption} services.autobar.enable
> :no-contents-entry:
> :no-index-entry:
> ```
