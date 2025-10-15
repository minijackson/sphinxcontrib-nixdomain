# Quick start

(full-example)=
## Full example

A fully working, flake-based example is available in <source:templates/example>,
which you can clone with:

``` bash
nix flake new -t "github:minijackson/sphinxcontrib-nixdomain#example" output-dir
```

## Import `sphinxcontrib-nixdomain`

### With flakes

Add `sphinxcontrib-nixdomain` to your flake inputs:

```{code-block} nix
:emphasize-lines: 5-8, 14

{
  # ...
 inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    sphinxcontrib-nixdomain = {
      url = "github:minijackson/sphinxcontrib-nixdomain";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    sphinxcontrib-nixdomain,
    # ...
  }:
  {
    # ...
  };
}
```

### Without flakes

TODO

## Create a Sphinx project

Create your Sphinx project by running:

``` bash
nix shell "nixpkgs#sphinx" -c sphinx-quickstart docs
```

Add `sphinxcontrib-nixdomain`, MyST, and Sphinx design
as Sphinx extensions in your documentation:

```{code-block} python
:caption: {file}`docs/conf.py`

extensions = [
    "sphinxcontrib_nixdomain",
    "sphinx_design",
    "myst_parser",
]

# -- Options for the MyST parser ---------------------------------------------
# https://myst-parser.readthedocs.io/en/latest/configuration.html

# These syntax extensions are required by `sphinxcontrib-nixdomain`
myst_enable_extensions = ["colon_fence", "fieldlist"]
```

Optionally, implement the {confval}`nixdomain_linkcode_resolve`
to have `[source]` links next to your objects:

```{code-block} python
:caption: {file}`docs/conf.py`

from urllib.parse import urlsplit

from sphinx.util import logging

logger = logging.getLogger(__name__)

# [Rest of the configuration...]

def nixdomain_linkcode_resolve(path: str) -> str:
    url = urlsplit(path)
    fragment = "#" + url.fragment if url.fragment else ""

    match url.netloc:
        case "self":
            return f"https://example.com/blob/master{url.path}{fragment}"
        case "nixpkgs":
            return f"https://github.com/NixOS/nixpkgs/blob/master{url.path}{fragment}"

    logger.warning("no source repository for url: %s", path)
    return ""
```

## Build the documentation with Nix

Add the `sphinxcontrib-nixdomain` overlay to your package set


```{code-block} nix
pkgs = import nixpkgs {
  # ...
  overlays = [
    # ...
    sphinxcontrib-nixdomain.overlays.default
  ];
};
```

Create a package that builds your Sphinx documentation:

```{code-block} nix
:caption: {file}`docs.nix`

{
  stdenvNoCC,
  lib,
  python3,
  nixdomainObjects,
}:
stdenvNoCC.mkDerivation {
  pname = "my-project-docs";
  version = "0.0.1-beta2";

  src = ../docs;

  nativeBuildInputs = with python3.pkgs; [
    myst-parser
    sphinx
    sphinx-design
    sphinxcontrib-nixdomain
  ];

  dontConfigure = true;

  buildPhase = ''
    runHook preBuild
    make html
    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall
    mkdir -p $out/share/doc/my-project/
    cp -r _build/html $out/share/doc/my-project/
    runHook postInstall
  '';

  env.NIXDOMAIN_OBJECTS = nixdomainObjects;

  meta = {
    description = "My super documentation";
    # ...
  };
}
```

And pass the objects to document
by using the {nix:func}`nixdomainLib.documentObjects` function:

```{code-block} nix
docs = pkgs.callPackage ./docs.nix {
  nixdomainObjects = sphinxcontrib-nixdomain.lib.documentObjects {
    sources = {
      self = self.outPath;
      nixpkgs = nixpkgs.outPath;
    };
    options.options = myNixosOptions;
    packages.packages = self.packages.x86_64-linux;
    library = {
      # Choosing a name different than "lib" is recommended,
      # to avoid confusion with Nixpkgs' "lib"
      name = "myLib";
      library = self.lib;
    };
  };
};
```

## Write the documentation

Next up is for you to write your documentation,
using {doc}`directives <../reference/auto-directives>`
for documenting your objects,
and {doc}`roles <../reference/roles>` for cross-referencing them.

See the {doc}`examples <../examples/auto-options>`
and the {doc}`cross-references` guide
for more information.
You can also look at the <project:#full-example>.

:::{seealso}
The {external+myst:doc}`MyST documentation <index>`
for the extended Markdown syntax documentation.

The {external+myst:doc}`Sphinx documentation <index>`
for general Sphinx concepts.
:::
