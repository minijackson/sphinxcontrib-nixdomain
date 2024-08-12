{ lib, pkgs, ... }:
{
  options.services.autobar = {
    enable = lib.mkEnableOption "the Bar service";

    package = lib.mkPackageOption pkgs "hello" { };
  };

  config = {
    # ...
  };
}
