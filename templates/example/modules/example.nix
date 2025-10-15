{lib, ... }:
{
  options.services.example.enable = lib.mkEnableOption "example service";
}
