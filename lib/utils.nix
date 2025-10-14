{ lib, ... }:

{
  /**
    Convert a path that's inside the Nix store
    to a URL to be passed to {confval}`nixdomain_linkcode_resolve`.

    :param attrset of str sources: the available sources to replace
    :param str path: the path whose prefix to replace
    :returns: the path with the prefix replaced
  */
  pathToURL =
    sources:
    let
      prefixes = lib.attrValues sources;
      replacements = map (name: "//${name}") (lib.attrNames sources);
    in
    lib.replaceStrings prefixes replacements;
}
