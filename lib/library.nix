{ lib, nixdomainLib, ... }:

{
  /**
    Document the given functions.

    :::{tip}
    This function is called by {nix:func}`nixdomainLib.documentObjects`
    with its `library` attribute value.
    There is no need to call it directly,
    pass the arguments of this function
    to the `library` attribute
    of the {nix:func}`nixdomainLib.documentObjects` function.
    :::

    :type:
      ```
      { sources; library; name; } -> list
      ```

    :param attrSet of strings sources: see {nix:func}`nixdomainLib.documentObjects`.
    :param attrSet of functions library:
      the set of functions to document.
      Recurses into children attribute sets
      and ignores undocumented functions.
    :param string name:
      The name/prefix of the library.
      Defaults to `"lib"`.
    :returns:
      a list of `nixdoc` invocations
      to be run by {nix:func}`nixdomainLib.documentObjects`,
      which is then usable by the `sphinxcontrib-nixdomain` Sphinx extension.
  */
  document =
    {
      sources,
      library ? { },
      name ? "lib",
    }:
    let
      libraryName = name;

      pathToURL = nixdomainLib.utils.pathToURL sources;

      /**
        A list of `{ name = loc; value = pos; }` of the given library

        Where `loc` is an array representing the attribute location
        in the library, e.g. `[ "options" "filter" ]` for `{options.filter = ...;}`

        And `pos` is the result of the `unsafeGetAttrPos` builtin,
        the location of the attribute on the disk (file, line, column).
      */
      funcLocations =
        let
          recurse =
            path: set:
            lib.flatten (
              lib.mapAttrsToList (
                name: value:
                if lib.isAttrs value then
                  recurse (path ++ [ name ]) value
                else
                  lib.nameValuePair (path ++ [ name ]) (builtins.unsafeGetAttrPos name set)
              ) set
            );
        in
        recurse [ ] library;

      funcLocation =
        { name, value }:
        {
          name =
            let
              libName = lib.optional (libraryName != "") libraryName;
            in
            lib.showOption (libName ++ name);
          value = if value ? file then pathToURL value.file else null;
        };

      /**
        The positions of the functions in the library,
        as required by the `nixdoc` `--locs` option.
      */
      locs = lib.pipe funcLocations [
        (lib.map funcLocation)
        lib.listToAttrs
        builtins.toJSON
        (builtins.toFile "locs.json")
      ];

      /**
        For all declared `sources` add them to the given string as context.

        This is so that the source is added as build input when running nixdoc,
        else it won't be able to read source files.
      */
      addContext = str: lib.pipe str (map lib.addContextFrom (lib.attrValues sources));

      /**
        Command-line arguments for `nixdoc`
      */
      nixdocInvocation =
        file: category:
        addContext (
          lib.cli.toGNUCommandLineShell { } {
            inherit file category;
            json-output = true;
            description = "";
            prefix = libraryName;
            locs = "${locs}";
          }
        );

      /**
        Like `listToAttrs`, but add a nice warning on duplicates,
        and choose the correct one.
      */
      listToAttrsWarn = lib.foldl' (
        acc:
        { name, value }:
        let
          previousValue = acc.${name};
          isAlreadyInThere = acc ? ${name} && value != previousValue;
          fileForWarn = pathToURL name;
          preferredValue =
            if lib.hasPrefix "${value}." previousValue then
              value
            else if lib.hasPrefix "${previousValue}." value then
              previousValue
            else
              null;
          hasNoPreferredValue = preferredValue == null;
        in
        if isAlreadyInThere then
          if hasNoPreferredValue then
            lib.warn ''
              File '${fileForWarn}' declares functions under both scope '${previousValue}' and '${value}',
                could not figure out a preferred scope, choosing '${previousValue}'.'' acc
          else
            lib.warn
              ''
                File '${fileForWarn}' declares functions under both scope '${previousValue}' and '${value}',
                  choosing '${preferredValue}' as it's a parent of the other.
                  Functions under the children scope probably won't be documented.
                  Extract those functions to a separate file, or don't export them to remove this warning.''
              (acc // { ${name} = preferredValue; })
        else
          acc // { ${name} = value; }
      ) { };

      nixdocInvocations = lib.pipe funcLocations [
        (lib.map (
          { name, value }:
          {
            name = value.file;
            value = lib.showOption (lib.sublist 0 (lib.length name - 1) name);
          }
        ))
        listToAttrsWarn
        (lib.mapAttrsToList nixdocInvocation)
      ];
    in
    {
      inherit nixdocInvocations;
    };
}
