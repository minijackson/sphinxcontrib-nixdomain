{ lib, ... }@args:

lib.fix (self: {
  /**
    Document the given packages.

    :::{tip}
    This function is called by {nix:func}`nixdomainLib.documentObjects`
    with its `packages` attribute value.
    There is no need to call it directly,
    pass the arguments of this function
    to the `packages` attribute
    of the {nix:func}`nixdomainLib.documentObjects` function.
    :::

    :type:
      ```
      {
        sources;
        packages;
        filters;
        extraFilters;
        modifiers;
        extraModifiers;
        metaAttributes;
      } -> attrSet
      ```

    :param attrSet of strings sources: see {nix:func}`nixdomainLib.documentObjects`.
    :param attrSet of packages packages:
      the set of packages to document.
      Follows the `lib.recurseIntoAttrs` indicator
      when recursing into children attribute sets.
    :param list of (package -> bool) functions filters:
      a list of function that filters the set of packages to document.
      By default,
      no filter is applied.
    :param list of (package -> bool) functions extraFilters:
      extra filters to apply in addition to `filters`.
    :param list of (package -> package) functions modifiers:
      apply this list of function to each package.
      By default,
      make the package declaration relative to the given `sources`,
      and keep only the tier 1 and tier 2 platforms
      in `platforms` attribute.
    :param list of (package -> package) functions extraModifiers:
      extra modifiers to apply in addition to `modifiers`.
    :returns:
      an attribute set of packages,
      usable by the `sphinxcontrib-nixdomain` Sphinx extension.
  */
  document =
    {
      sources,
      packages ? { },
      filters ? [ ],
      extraFilters ? [ ],
      modifiers ? [
        (self.modifiers.relativePosition sources)
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

  /**
    The list of Nixpkgs tier 1 platforms.

    :type: `list of strings`
  */
  tier1Platforms = [
    "x86_64-linux"
  ];

  /**
    The list of Nixpkgs tier 2 platforms.

    :type: `list of strings`
  */
  tier2Platforms = [
    "aarch64-linux"
    "x86_64-darwin"
  ];

  /**
    Collect information about a given package, with the given meta attributes.

    :type: `metaAttrs :: list -> pkg :: package -> package`
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
