{ lib, nixdomainLib, ... }:
{
  /**
    URLify the position of the given package.

    :type: `sources :: attrSet -> pkg :: package -> package`
    :param attrset of str sources: the available sources to replace
    :param package pkg: the package whose position to change
    :returns: the modified package
  */
  relativePosition =
    sources: pkg:
    if !pkg.meta ? position then
      pkg
    else
      pkg
      // {
        meta = pkg.meta // {
          position =
            let
              posElements = lib.splitString ":" pkg.meta.position;
              filePos = lib.elemAt posElements 0;
              linePos = lib.elemAt posElements 1;
              lineFragment = lib.optionalString (lib.length posElements >= 2) "#L${linePos}";
              pos = "${filePos}${lineFragment}";
            in
            nixdomainLib.utils.pathToURL sources pos;
        };
      };

  /**
    Change the package's declared platform to only show the given ones.

    This function is useful to limit the shown platforms to only the supported ones.

    :type: `shownPlatforms :: list -> pkg :: package -> package`
    :param list of str shownPlatforms: the platforms to show
    :param package pkg: the package to change
    :returns: the modified package
  */
  filterPlatforms =
    shownPlatforms: pkg:
    if !pkg.meta ? platforms then
      pkg
    else
      pkg
      // {
        meta = pkg.meta // {
          platforms = lib.filter (platform: lib.elem platform shownPlatforms) pkg.meta.platforms;
        };
      };
}
