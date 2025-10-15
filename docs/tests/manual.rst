Manual declarations
===================

Functions
---------

.. nix:function:: toString
   :no-index-entry:

   Convert the given value to a string

   .. code-block:: nix
      :caption: Example

      nix> toString 42
      "42"

Packages
--------

.. nix:package:: python3Packages.bla
   :no-index-entry:

   Hello this is a description.

   :name: bla
   :version: 0.0.0-rc1
   :license: Bla
   :maintainers: Myself
   :override bool withEncryption: support encryption
   :override list of strings features: features to enable

NixOS-like module options
-------------------------

.. seealso::

   Example of ref links:

   - :nix:obj:`services.foo.enable`
   - :nix:option:`services.bar.enable`
   - :nix:bind:`toString`

   And failing examples:

   - :nix:option:`services.nonexistent.enable`
   - :nix:bind:`missingFunction`
   - :nix:obj:`missingObject`

Service Foo
^^^^^^^^^^^

.. nix:option:: services.foo.enable
   :no-index-entry:

   Enable the Foo service

   .. code-block:: nix
      :caption: Default value

      false

   .. code-block:: nix
      :caption: Example

      true


.. nix:option:: services.foo.settings
   :no-index-entry:
   :type: submodule

   Settings for Foo

   .. code-block:: nix
      :caption: Default value

      {}

   .. code-block:: nix
      :caption: Example

      {
         baz = [ "one" ];
      }


.. nix:option:: services.foo.settings.baz
   :no-index-entry:
   :type: list of (string)
   :read-only:

   List of config to handle

   .. code-block:: nix
      :caption: Default value

      []

   .. code-block:: nix
      :caption: Example

      [ "one" "two" "three" ]

Service Bar
^^^^^^^^^^^

.. nix:option:: services.bar
   :no-index-entry:
   :type: submodule

   .. nix:option:: enable
      :no-index-entry:

      Enable the Bar service

      .. code-block:: nix
         :caption: Default value

         false

      .. code-block:: nix
         :caption: Example

         true


   .. nix:option:: settings
      :no-index-entry:
      :type: attribute set

      Settings for Bar

      .. code-block:: nix
         :caption: Default value

         {}

      .. code-block:: nix
         :caption: Example

         {
            baz = [ "one" ];
         }


      .. nix:option:: baz
         :no-index-entry:
         :type: list of (string)

         List of config to handle

         .. code-block:: nix
            :caption: Default value

            []

         .. code-block:: nix
            :caption: Example

            [ "one" "two" "three" ]


Python
------

.. py:module:: TheModule
   :no-index-entry:

   Hello

   .. py:class:: TheClass(int, float)
      :no-index-entry:

      .. py:class:: Thing
         :no-index-entry:

         .. py:method:: bla(str, list[str])
            :no-index-entry:

   .. py:class:: Thing
      :no-index-entry:

      .. py:method:: bla(str, list[str])
         :no-index-entry:
