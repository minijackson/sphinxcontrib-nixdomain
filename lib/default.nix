{ lib, pkgs, nixdomainLib, ... }@args:

{
  /**
    Document the given objects.

    :param attrSet options:
      The set of options to document,
      see {func}`options.document` for more information
    :param attrSet of documentable packages packages:
      The set of packages to document,
      see {func}`packages.document` for more information.
    :returns:
      a JSON file used by the sphinxcontrib-nixdomain Sphinx extension,
      to be passed through the {envvar}`NIXDOMAIN_OBJECTS` environment variable.
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
