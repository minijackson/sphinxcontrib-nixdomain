Cross-references
================

.. note::

   With Intersphinx,
   these cross-references can resolve to objects
   defined in an external Sphinx project.

.. rst:role:: nix:obj

   Refer to any object defined by sphinxcontrib-nixdomain.

   For example::

      See the :nix:obj:`services.foo.enable` object.

   Is rendered as:

      See the :nix:obj:`services.foo.enable` object.

.. rst:role:: nix:option

   Refer to an option from the NixOS module system.

   For example::

      See the :nix:option:`services.foo.enable` option.

   Is rendered as:

      See the :nix:option:`services.foo.enable` option.

.. rst:role:: nix:pkg

   Refer to a Nix package.

   For example::

      See the :nix:pkg:`python3Packages.bla` package.

   Is rendered as:

      See the :nix:pkg:`python3Packages.bla` package.
