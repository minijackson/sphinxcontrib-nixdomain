{ lib, ... }:
{
  /**
    Returns whether the given option should be visible in the documentation.

    :type: `option :: option -> bool`
    :param option option: the option to check
  */
  isVisible = option: !option.internal;

  /**
    Returns whether the given option is declared in the given directory.

    :type: `prefix :: string -> option :: option -> bool`
    :param string prefix: the directory where the option should be declared
    :param option option: the option to check
  */
  isDeclaredIn = prefix: option: lib.any (lib.hasPrefix prefix) option.declarations;
}
