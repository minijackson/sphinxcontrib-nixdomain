{ lib, nixdomainLib, ... }:
{
  /**
    URLify the declarations of the given option.

    :param attrset of str sources: the available sources to replace
    :param option option: the option whose declarations to change
    :returns: the modified option
  */
  relativeDeclaration =
    sources: option:
    option // { declarations = map (nixdomainLib.utils.pathToURL sources) option.declarations; };
}
