# Markdown autodoc examples

Remember to set the `default-domain` to `nix` in your Markdown files
if your options use the `` {option}`services.foo.enable` `` syntax.

You can do it like so:

````markdown
```{default-domain} nix
```
````

```{default-domain} nix
```

## NixOS-like module options

### Using `autooption`

```{autooption} services.autobar.enable
```

### Using `automodule`

```{nix:automodule} services.autobar
```

## Nix packages

### Using `autopackage`

```{autopackage} example1
```

```{autopackage} hello
```

```{autopackage} scope.nimScript
```

### Using `autopackages`

```{autopackages}
```
