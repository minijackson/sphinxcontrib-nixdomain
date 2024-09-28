Manual example
==============

.. TODO: explain more, present functions used

Functions
---------

.. nix:function:: toString

   Convert the given value to a string

   .. code-block:: nix
      :caption: Example

      nix> toString 42
      "42"


NixOS-like module options
-------------------------

.. seealso::

   Example of ref links:

   - :nix:ref:`services.foo.enable`
   - :nix:option:`services.bar.enable`
   - :nix:bind:`toString`

   And failing examples:

   - :nix:option:`services.nonexistent.enable`
   - :nix:bind:`missingFunction`

Service Foo
^^^^^^^^^^^

.. nix:option:: services.foo.enable

   Enable the Foo service

   .. code-block:: nix
      :caption: Default value

      false

   .. code-block:: nix
      :caption: Example

      true


.. nix:option:: services.foo.settings
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
   :type: submodule
   :no-index-entry:

   .. nix:option:: enable

      Enable the Bar service

      .. code-block:: nix
         :caption: Default value

         false

      .. code-block:: nix
         :caption: Example

         true


   .. nix:option:: settings
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

   Hello

   .. py:class:: TheClass(int, float)

      .. py:class:: Thing

         .. py:method:: bla(str, list[str])

   .. py:class:: Thing

      .. py:method:: bla(str, list[str])
