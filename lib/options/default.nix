{ lib, ... }@args:

lib.fix (self: {
  /**
    Document the given options.

    :::{tip}
    This function is called by {nix:func}`nixdomainLib.documentObjects`
    with its `options` attribute value.
    There is no need to call it directly,
    pass the arguments of this function
    to the `options` attribute
    of the {nix:func}`nixdomainLib.documentObjects` function.
    :::

    :type:
      ```
      {
        sources;
        options;
        filters;
        extraFilters;
        modifiers;
        extraModifiers;
      } -> attrSet
      ```

    :param attrSet of strings sources: see {nix:func}`nixdomainLib.documentObjects`.
    :param attrSet of options options:
      the set of options to document,
      as returned by `(lib.nixosSystem { ... }).options`.
    :param list of (option -> bool) functions filters:
      a list of function that filters the set of options to document.
      By default,
      keep only visible options
      that are declared in the `self` source.
    :param list of (option -> bool) functions extraFilters:
      extra filters to apply in addition to `filters`.
    :param list of (option -> option) functions modifiers:
      apply this list of function to each option.
      By default,
      make the option declarations relative to the given `sources`.
    :param list of (option -> option) functions extraModifiers:
      extra modifiers to apply in addition to `modifiers`.
    :returns:
      an attribute set of options,
      usable by the `sphinxcontrib-nixdomain` Sphinx extension.
  */
  document =
    {
      sources,
      options ? { },
      filters ? [
        self.filters.isVisible
        (self.filters.isDeclaredIn sources.self)
      ],
      extraFilters ? [ ],
      modifiers ? [
        (self.modifiers.relativeDeclaration sources)
      ],
      extraModifiers ? [ ],
    }:
    lib.pipe options (
      [ self.attrSetToDocList ]
      ++ map lib.filter filters
      ++ map lib.filter extraFilters
      ++ map map modifiers
      ++ map map extraModifiers
      ++ [
        (map (x: lib.nameValuePair x.name x))
        lib.listToAttrs
      ]
    );

  filters = import ./filters.nix args;
  modifiers = import ./modifiers.nix args;

  /**
    Generate documentation template from the list of option declaration like
    the set generated with filterOptionSets.

    Originally taken from nixpkgs' `lib.optionAttrSetToDocList`.
  */
  attrSetToDocList =
    options:
    lib.concatMap (
      opt:
      let
        name = lib.showOption opt.loc;
        docOption = {
          inherit (opt) loc;
          inherit name;
          description = opt.description or null;
          declarations = lib.filter (x: x != lib.unknownModule) opt.declarations;
          internal = opt.internal or false;
          visible = if (opt ? visible && opt.visible == "shallow") then true else opt.visible or true;
          read_only = opt.readOnly or false;
          typ = opt.type.description or "unspecified";
          example =
            if opt ? example then
              builtins.addErrorContext "while evaluating the example of option `${name}`" (
                self.renderOptionValue opt.example
              )
            else
              null;
          default =
            if (opt ? defaultText || opt ? default) then
              builtins.addErrorContext "while evaluating the ${
                if opt ? defaultText then "defaultText" else "default value"
              } of option `${name}`" (self.renderOptionValue (opt.defaultText or opt.default))
            else
              null;
          related_packages = opt.relatedPackages or null;
        };

        subOptions =
          let
            ss = opt.type.getSubOptions opt.loc;
          in
          if ss != { } then self.attrSetToDocList ss else [ ];
        subOptionsVisible = docOption.visible && opt.visible or null != "shallow";
      in
      # To find infinite recursion in NixOS option docs:
      # builtins.trace opt.loc
      [ docOption ] ++ lib.optionals subOptionsVisible subOptions
    ) (lib.collect lib.isOption options);

  /**
    Ensures that the given option value (default or example) is a string
    by rendering Nix values.
  */
  renderOptionValue =
    v:
    if v ? _type && v ? text then
      v.text
    else
      lib.generators.toPretty {
        multiline = true;
        allowPrettyValues = true;
      } v;
})
