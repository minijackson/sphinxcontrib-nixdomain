{ lib, ... }:

lib.fix (self: {
  /**
    :param str prefix: TODO
  */
  document =
    {
      sources,
      library ? { },
      name ? "lib",
      prefix,
    }:
    let
      libraryName = name;

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
          value = if value ? file then lib.removePrefix prefix value.file else null;
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
        Command-line arguments for `nixdoc`
      */
      nixdocInvocation =
        file: category:
        lib.addContextFrom prefix (
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
})
