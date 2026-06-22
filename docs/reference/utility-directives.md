# Utility directives

::::::{rst:directive} .. nix:currentmodule:: module

Make the nixdomain plugin believe
that you are in the NixOS module `module`.
This makes the nixdomain plugin resolve NixOS option cross-references
from the given `module` first.

For an example usage, see {ref}`currentmodule-example`.

::::::
