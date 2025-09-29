args:

{
  /**
    Document the given objects.

    :param attrSet of documentable options options:
      The set of options to document, as returned by {func}`options.document`.
    :returns:
      a JSON file used by the sphinxcontrib-nixdomain Sphinx extension,
      to be passed through the {env}`NIXDOMAIN_OBJECTS` environment variable.
  */
  documentObjects =
    {
      options ? { },
    }@args:
    builtins.toFile "nix-objects.json" (builtins.toJSON args);

  options = import ./options args;

}
