{
  description = "Nix domain and autodoc for Sphinx";

  inputs = {
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
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
      # For some reason, build crashes on doctree-read event with Python3.12
      python = pkgs.python3;
    in
    {
      devShells.x86_64-linux.default =
        let
          arg = project.renderers.withPackages {
            inherit python;
            extras = [ "docs" ];
          };
          pythonEnv = python.withPackages arg;
        in
        pkgs.mkShell {
          packages = [
            pythonEnv
            pkgs.hatch
          ];
        };

      packages.x86_64-linux = {
        default = self.packages.x86_64-linux.sphinxcontrib-nixdomain;
        sphinxcontrib-nixdomain =
          let
            attrs = project.renderers.buildPythonPackage {
              inherit python;
              extras = [ "docs" ];
            };
          in
          (python.pkgs.buildPythonPackage attrs).overrideAttrs (old: {
            nativeBuildInputs = old.nativeBuildInputs or [ ] ++ [ python.pkgs.sphinxHook ];
          });
      };
    };
}
