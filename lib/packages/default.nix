{ lib, ... }@args:

lib.fix (self: {
  /**
    :param str prefix: TODO

    TODO: make sure to convert `prefix` to string, and add a trailing slash.
    Or, we normalize the prefix.
  */
  document =
    {
      prefix,
      packages ? { },
      filters ? [ ],
      extraFilters ? [ ],
      modifiers ? [
        # TODO: find a solution for linking to multiple sources
        (self.modifiers.relativePosition prefix)
        (self.modifiers.filterPlatforms (self.tier1Platforms ++ self.tier2Platforms))
      ],
      extraModifiers ? [ ],
      metaAttributes ? [
        "description"
        "longDescription"
        "branch"
        "homepage"
        "downloadPage"
        "changelog"
        "license"
        "sourceProvenance"
        "maintainers"
        "teams"
        "platforms"
        "broken"
        "unfree"
        "insecure"
        "knownVulnerabilities"
        "badPlatforms"
        "position"
      ],
    }:
    self.collect {
      inherit metaAttributes packages;
      filters = filters ++ extraFilters;
      modifiers = modifiers ++ extraModifiers;
    };

  modifiers = import ./modifiers.nix args;

  # Source: https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md
  tier1Platforms = [
    "x86_64-linux"
  ];
  tier2Platforms = [
    "aarch64-linux"
    "x86_64-darwin"
  ];

  /**
    Collect information about a given package, with the given meta attributes.

    :param list of str metaAttrs: the meta attributes to collect for the given package
    :param package pkg: the package to collect information from
  */
  collectPackage =
    metaAttrs: pkg:
    let
      maybeInherit = set: attrs: lib.filterAttrs (name: _value: lib.elem name attrs) set;
    in
    {
      name = pkg.pname or pkg.name;
      version = pkg.version or null;
    }
    // {
      meta = maybeInherit pkg.meta metaAttrs;
    };

  /**
    Collect all packages recursively,
    into an attribute set of `loc` -> `derivation`.

    Respects Nixpkgs's `recurseIntoAttrs`.

    Inspired by flake-utils' flattenTree.

    :param list of str metaAttrs: the meta attributes to collect for each package
    :param attribute set set: the set containing the packages to collect
  */
  collect =
    {
      metaAttributes,
      packages,
      filters,
      modifiers,
    }:
    let
      passesFilters = pkg: lib.foldl' (acc: filter: acc && filter pkg) true filters;
      # passesFilters = pkg: lib.all (check: check) (map (filter: filter pkg) filters);
      modify = pkg: lib.pipe pkg modifiers;
      op =
        sum: loc: maybeVal:
        let
          evalResult = builtins.tryEval maybeVal;
          val = evalResult.value;
        in
        if !evalResult.success || (builtins.typeOf val) != "set" then
          # Ignore non-sets
          sum
        else if val ? type && val.type == "derivation" && passesFilters val then
          # Add the derivation
          sum
          // {
            "${lib.showOption loc}" = (self.collectPackage metaAttributes (modify val)) // {
              inherit loc;
            };
          }
        else if val ? recurseForDerivations && val.recurseForDerivations then
          # Recurse into that attribute set
          recurse sum loc val
        else
          # Ignore anything else
          sum;

      recurse =
        sum: loc: subtree:
        lib.foldlAttrs (
          sum: key: val:
          op sum (loc ++ [ key ]) val
        ) sum subtree;
    in
    recurse { } [ ] packages;
})
