{
  description = "Nix domain and autodoc for Sphinx";

  inputs = {
    flake-compat.url = "github:edolstra/flake-compat";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      pyproject-nix,
      ...
    }:
    let
      project = pyproject-nix.lib.project.loadPyproject { projectRoot = ./.; };
      pkgs = import nixpkgs {
        system = "x86_64-linux";
        overlays = [ self.overlays.default ];
      };
    in
    {
      lib = nixpkgs.lib.fix (
        nixdomainLib:
        import ./lib {
          inherit (nixpkgs) lib;
          inherit pkgs nixdomainLib;
        }
      );

      packages.x86_64-linux = {
        inherit (pkgs.python3.pkgs) sphinxcontrib-nixdomain;
        default = self.packages.x86_64-linux.sphinxcontrib-nixdomain;

        exampleObjectsJson =
          let
            inherit (nixpkgs) lib;

            config = lib.nixosSystem {
              modules = import ./examples/options/modules-list.nix;
              system = "x86_64-linux";
            };
            inherit (config) options;
          in
          self.lib.documentObjects {
            sources = {
              self = self.outPath;
              nixpkgs = nixpkgs.outPath;
            };
            options.options = options;
            packages.packages = import ./examples/packages pkgs;
            library = {
              name = "";
              library = {
                nixdomainLib = self.lib;
                exampleLib = import ./examples/library;
              };
            };
          };
      };

      overlays.default = _final: prev: {
        pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [
          (final: _prev: {
            sphinxcontrib-nixdomain =
              let
                inherit (final) python;
                attrs = project.renderers.buildPythonPackage {
                  inherit python;
                  extras = [ "docs" ];
                  extrasAttrMappings.docs = "nativeBuildInputs";
                };
              in
              (python.pkgs.buildPythonPackage attrs).overrideAttrs (old: {
                nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [
                  python.pkgs.sphinxHook
                  python.pkgs.pytestCheckHook
                ];

                env = {
                  REVISION = self.rev or "main";
                  NIXDOMAIN_OBJECTS = self.packages.x86_64-linux.exampleObjectsJson;
                  SOURCE_DATE_EPOCH = self.sourceInfo.lastModified;
                };
              });
          })
        ];
      };

      templates.example = {
        path = ./templates/example;
        description = "An example project using sphinxcontrib-nixdomain";
      };
    };
}
