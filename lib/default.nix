{ lib, ... }:

rec {
  # Originallly taken from nixpkgs.lib.optionAttrSetToDocList

  /**
    Generate documentation template from the list of option declaration like
    the set generated with filterOptionSets.
  */
  optionAttrSetToDocList =
    options:
    lib.concatMap (
      opt:
      let
        name = lib.showOption opt.loc;
        docOption = {
          # inherit (opt) loc;
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
                renderOptionValue opt.example
              )
            else
              null;
          default =
            if (opt ? defaultText || opt ? default) then
              builtins.addErrorContext "while evaluating the ${
                if opt ? defaultText then "defaultText" else "default value"
              } of option `${name}`" (renderOptionValue (opt.defaultText or opt.default))
            else
              null;
          related_packages = opt.relatedPackages or null;
        };

        subOptions =
          let
            ss = opt.type.getSubOptions opt.loc;
          in
          if ss != { } then optionAttrSetToDocList ss else [ ];
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

}
