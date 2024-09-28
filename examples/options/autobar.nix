{ lib, pkgs, ... }:
{
  imports = [
    (lib.mkRenamedOptionModule
      [
        "services"
        "autobar"
        "pkg"
      ]
      [
        "services"
        "autobar"
        "package"
      ]
    )
  ];

  options.services.autobar = {
    enable = lib.mkEnableOption "the Bar service";

    package = lib.mkPackageOption pkgs "hello" { };

    openFirewall = lib.mkOption {
      description = ''
        Whether to automatically open the firewall.

        ```{warning}
        This opens the firewall on all network interfaces.
        ```

        ```{versionadded} nixos-24.05
        ```
      '';
      default = false;
      example = true;
    };
  };

  config = {
    # ...
  };
}
