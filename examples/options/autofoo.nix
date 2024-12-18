{ lib, pkgs, ... }:
{
  options.services.autofoo = {
    enable = lib.mkEnableOption "the Foo service";

    package = lib.mkPackageOption pkgs "hello" { };

    settings = lib.mkOption {
      description = ''
        Settings for the Foo service.

        .. versionadded:: nixos-24.05

        .. seealso::

           :option:`autobar`
      '';

      default = { };

      type = lib.types.submodule {
        freeformType = (pkgs.formats.toml { }).type;

        options = {
          bar.bar.baz = lib.mkOption {
            description = "How to configure bar's ``baz``";
            default = [ ];
            example = [
              "hello"
              "world"
            ];
            type = with lib.types; listOf str;
          };

          "com.package/config" = lib.mkOption {
            readOnly = true;
          };
        };
      };
    };
  };

  config = {
    # ...
  };
}
