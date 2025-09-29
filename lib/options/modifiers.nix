{ lib, ... }:
{
  /**
    URLify the declarations of the given option.

    :param attrset of str sources: the available sources to replace
    :param option option: the option whose declarations to change
    :returns: the modified option
  */
  relativeDeclaration =
    prefix: option:
    option
    // {
      declarations = map (lib.removePrefix prefix) (
        lib.filter (lib.hasPrefix prefix) option.declarations
      );
    };
}
