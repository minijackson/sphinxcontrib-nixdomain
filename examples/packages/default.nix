pkgs: {
  inherit (pkgs) hello;

  example1 = pkgs.callPackage (
    {
      myFeature ? false,
      modules ? [
        "module1"
        "module2"
      ],
    }:
    pkgs.stdenv.mkDerivation {
      pname = "example1";
      version = "0.1.0";

      # ...

      meta = {
        description = "An example package";
        longDescription = ''
          More information can be added in the `longDescription` meta attribute.

          You can also use field lists to document things like overrides:

          :override bool myFeature: whether to enable my feature
          :override list of str modules: modules to compile
        '';
        broken = true;
        knownVulnerabilities = [ "hello" ];
        license = [pkgs.lib.licenses.unfree];
        platforms = [ ];
      };
    }
  ) { };

  scope = pkgs.lib.recurseIntoAttrs {
    nimScript = pkgs.callPackage (_: pkgs.writers.writeNimBin "test" { } "") { };
    "special name" = pkgs.hello;
  };
}
