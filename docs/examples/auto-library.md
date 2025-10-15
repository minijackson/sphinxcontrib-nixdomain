# Automatic library

```{default-domain} nix
```

:::{tip}
Click the `[source]` link next to the object
to open the declaration source file.

Click the eye icon in the upper-right of the page
to open the Markdown source file.
:::

(library-example)=
## Document a function library

To document a whole set of functions,
use the {rst:dir}`nix:autolibrary` directive.

### Document everything

To document every function found,
don't pass any argument to the directive.

For example:

``````markdown
```{default-domain} nix
```

```{autolibrary}
```
``````

Renders:

> ```{autolibrary} exampleLib
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

```{autolibrary} exampleLib.scope
```
``````

Renders:

> ```{autolibrary} exampleLib.scope
> :no-contents-entry:
> :no-index-entry:
> ```

(function-example)=
## Document a single function

To document a single function,
use the {rst:dir}`nix:autofunction` directive.

For example:

``````markdown
```{default-domain} nix
```

```{autofunction} exampleLib.myFunc
```
``````

Renders:

> ```{autofunction} exampleLib.myFunc
> :no-contents-entry:
> :no-index-entry:
> ```
