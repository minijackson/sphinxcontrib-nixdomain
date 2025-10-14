{ lib, pkgs, ... }@args:

lib.fix (self: {
  /**
    Document the given objects.

    :param attrSet of documentable options options:
      The set of options to document, as returned by {func}`options.document`.
    :param attrSet of documentable packages packages:
      The set of packages to document,
      see {func}`packages.document` for more information.
    :returns:
      a JSON file used by the sphinxcontrib-nixdomain Sphinx extension,
      to be passed through the {env}`NIXDOMAIN_OBJECTS` environment variable.
  */
  documentObjects =
    {
      prefix,
      options ? { },
      packages ? { },
      library ? { },
    }:
    let
      common = { inherit prefix; };
    in
    pkgs.callPackage ./build-objects-json.nix { } {
      options = self.options.document (common // options);
      packages = self.packages.document (common // packages);
      library = self.library.document (common // library);
    };

  library = import ./library.nix args;
  options = import ./options args;
  packages = import ./packages args;
})
