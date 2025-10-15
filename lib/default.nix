{ pkgs, nixdomainLib, ... }@args:

{
  /**
    Document the given objects.

    :type: `{ sources; options; packages; library; } -> store path`
    :param attrSet of strings sources:
      a {samp}`{source-name} -> {source-path}` attribute set.
      The source `self` is expected to be your project's root path.
    :param attrSet options:
      the set of options to document,
      forwarded to {func}`options.document`.
      See its documentation for more information.
    :param attrSet packages:
      the set of packages to document,
      forwarded to {func}`packages.document`.
      See its documentation for more information.
    :param attrSet library:
      the set of functions to document,
      forwarded to {func}`library.document`.
      See its documentation for more information.
    :returns:
      a JSON file used by the `sphinxcontrib-nixdomain` Sphinx extension,
      to be passed through the {envvar}`NIXDOMAIN_OBJECTS` environment variable.

    ```{code-block} nix
    :caption: Example usage

    lib.documentObjects {
      sources = {
        self = inputs.self.outPath;
        nixpkgs = inputs.nixpkgs.outPath;
      };
      options = {
        options =
          (inputs.nixpkgs.lib.nixosSystem {
            system = "x86_64-linux";
            modules = [ self.nixosModules.default ];
          }).options;
        extraFilters = [
          # Example filter: the option has a description
          (opt: opt ? description)
        ];
        packages.packages = inputs.self.packages.x86_64-linux;
        library = {
          # Choosing a name different than "lib" is recommended,
          # to avoid confusion with Nixpkgs' "lib"
          name = "myLib";
          library = inputs.self.lib;
        };
      };
    }
    ```
  */
  documentObjects =
    {
      sources,
      options ? { },
      packages ? { },
      library ? { },
    }:
    let
      common = { inherit sources; };
    in
    pkgs.callPackage ./build-objects-json.nix { } {
      options = nixdomainLib.options.document (common // options);
      packages = nixdomainLib.packages.document (common // packages);
      library = nixdomainLib.library.document (common // library);
    };

  library = import ./library.nix args;
  options = import ./options args;
  packages = import ./packages args;
  utils = import ./utils.nix args;
}
