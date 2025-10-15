# Automatic packages

```{default-domain} nix
```

:::{tip}
Click the `[source]` link next to the object
to open the declaration source file.

Click the eye icon in the upper-right of the page
to open the Markdown source file.
:::

(packages-example)=
## Document a package set

To document a whole set of package,
use the {rst:dir}`nix:autopackages` directive.

### Document everything

To document every package found,
don't pass any argument to the directive.

For example:

``````markdown
```{default-domain} nix
```

```{autopackages}
```
``````

Renders:

> ```{autopackages}
> :no-contents-entry:
> :no-index-entry:
> ```

### Document a subset

To render only a subset of function,
pass the desired scope to the directive.

For example:

``````markdown
```{default-domain} nix
```

```{autopackages} scope
```
``````

Renders:

> ```{autopackages} scope
> :no-contents-entry:
> :no-index-entry:
> ```

(package-example)=
## Document a single package

To document a single package,
use the {rst:dir}`nix:autopackage` directive.

For example:

``````markdown
```{default-domain} nix
```

```{autopackage} hello
```
``````

Renders:

> ```{autopackage} hello
> :no-contents-entry:
> :no-index-entry:
> ```
