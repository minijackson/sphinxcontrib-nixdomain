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
  /**
    Create a JSON with a single "library" attribute,
    which is an attribute set of function name -> functions.
  */
  jqNixDocFilter = ''
    {
      library: (
        [
          # For each entry of each nixdoc JSON file
          .[].entries[] |
          # Concatenate the full name, while taking care of ignoring empty strings
          ([.prefix, .category, .name] | map(select(. != "")) | join(".")) as $name |
          # Create an object for that function
          {
            ($name): {
              name: $name,
              description: .description | join("\n\n"),
              location: .location
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
in
runCommand "nix-objects.json"
  {
    nativeBuildInputs = [
      jq
      nixdoc
    ];
  }
  ''
    {
      # A dummy command, in case there's no nixdoc invocation
      :
      # TODO: handle failures
      ${lib.concatMapStringsSep "\n" (args: "nixdoc ${args} || true") library.nixdocInvocations}
    } | jq -cs '${jqNixDocFilter}' > library.json

    # Combine the JSON into a single one
    jq -cs add "${notLibrary}" library.json > $out
  ''
