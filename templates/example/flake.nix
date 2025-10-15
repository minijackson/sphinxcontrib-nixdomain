{
  description = "An example project using sphinxcontrib-nixdomain";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    sphinxcontrib-nixdomain = {
      url = "github:minijackson/sphinxcontrib-nixdomain";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      sphinxcontrib-nixdomain,
    }:
    {
      nixosModules.default = {
        imports = [ ./modules/example.nix ];
      };

      packages.x86_64-linux =
        let
          pkgs = import nixpkgs {
            system = "x86_64-linux";
            overlays = [ sphinxcontrib-nixdomain.overlays.default ];
          };
        in
        {
          hello = pkgs.hello;
          docs = pkgs.callPackage ./pkgs/docs.nix {
            nixdomainObjects = sphinxcontrib-nixdomain.lib.documentObjects {
              sources = {
                self = self.outPath;
                nixpkgs = nixpkgs.outPath;
              };
              options.options =
                (nixpkgs.lib.nixosSystem {
                  system = "x86_64-linux";
                  modules = [ self.nixosModules.default ];
                }).options;
              packages.packages = self.packages.x86_64-linux;
              library = {
                name = "myLib";
                library = self.lib;
              };
            };
          };
        };

      lib = import ./lib { inherit (nixpkgs) lib; };
    };
}
