{
  lib,
  runCommand,
  jq,
  nixdoc,
}:
{
  options ? { },
  packages ? { },
  library ? { },
}:

let
  jqSubstituteSources = toString (
    lib.mapAttrsToList (name: outpath: ''| sub("${outpath}"; "//${name}")'') library.sources
  );

  jqNixDocFilter = ''
    {
      library: (
        [
          # For each entry of the nixdoc JSON output
          .entries[] |
          # Substitute Nix store paths with the corresponding `//source` URL authority
          (.source.file ${jqSubstituteSources}) as $file |
          # Create an object for that function
          {
            (.attrPath): {
              name: .attrPath,
              description: .description,
              location: [$file, .source.line] | join("#L")
            }
          }
          # Merge the list of objects into a single object
        ] | add
        # Or the empty object, if the list is empty
        // {}
      )
    }
  '';

  notLibrary = builtins.toFile "notLibrary.json" (builtins.toJSON { inherit options packages; });
  nixdocManifest = builtins.toFile "nixdoc-manifest.json" (builtins.toJSON library.nixdocManifest);
in
runCommand "nix-objects.json"
  {
    nativeBuildInputs = [
      jq
      nixdoc
    ];
  }
  ''
    nixdoc --manifest "${nixdocManifest}" | jq -c '${jqNixDocFilter}' > library.json

    # Combine the JSON into a single one
    jq -cs add "${notLibrary}" library.json > $out
  ''
