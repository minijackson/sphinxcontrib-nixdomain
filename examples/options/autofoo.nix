{ lib, pkgs, ... }:
{
  options.services.autofoo = {
    enable = lib.mkEnableOption "the Foo service";

    package = lib.mkPackageOption pkgs "hello" { };

    settings = lib.mkOption {
      description = ''
        Settings for the Foo service.

        .. versionadded:: nixos-24.05
      '';

      default = { };

      type = lib.types.submodule {
        freeformType = (pkgs.formats.toml { }).type;

        options = {
          baz = lib.mkOption {
            description = "How to configure ``baz``";
            default = [ ];
            example = [
              "hello"
              "world"
            ];
            type = with lib.types; listOf str;
          };
        };
      };
    };
  };

  config = {
    # ...
  };
}
