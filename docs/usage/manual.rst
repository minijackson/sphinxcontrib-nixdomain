Manual declarations
===================

.. highlight:: rst

You can declare Nix objects manually
by using the following directives.

Use these directives when generating from Nix code isn't possible
or if you want to develop a custom documentation generator.

.. seealso::
   :doc:`../examples/manual-example` for more manual usage examples.

.. rst:directive:: .. nix:option:: name

   Describes a option from the NixOS module system.

   For example::

      .. nix:option:: service.my-service.enable

         My option description

   Is redendered as:

      .. nix:option:: service.my-service.enable
         :no-index:

         My option description

   .. rubric:: Options

   .. rst:directive:option:: type
      :type: text

      The type of the option,
      for example ``list of string``.

   .. rst:directive:option:: read-only

      Add this option of the option is read-only.

   .. rst:directive:option:: declaration
      :type: text

      A link to the source code.
      See the :confval:`nixdomain_linkcode_resolve` configuration
      to generate a ``[source]`` link.

   .. rst:directive:option:: short-toc-name

      Whether to show a short name in the table of contents.

   Other standard domain options are supported,
   see the Sphinx domain :ref:`Basic Markup <basic-domain-markup>` documentation.

.. rst:directive:: .. nix:package:: name

   Describes a Nix package.

   Use :ref:`field-lists <rst-field-lists>` after the description
   to describe the package's metadata

   For example::

      .. nix:package:: myProject.myPackage

         My package description

         :version: 0.0.0-rc1
         :license: EUPL-1.2

   Will be redendered as:

   .. nix:package:: myProject.myPackage
      :no-index:

      My package description

      :version: 0.0.0-rc1
      :license: EUPL-1.2

   .. rubric:: Options

   .. rst:directive:option:: declaration
      :type: text

      A link to the source code.
      See the :confval:`nixdomain_linkcode_resolve` configuration
      to generate a ``[source]`` link.

   .. rst:directive:option:: short-toc-name

      Whether to show a short name in the table of contents.

   Other standard domain options are supported,
   see the Sphinx domain :ref:`Basic Markup <basic-domain-markup>` documentation.
