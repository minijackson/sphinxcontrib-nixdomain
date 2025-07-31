Configuration
=============

.. role:: code-py(code)
   :language: Python

.. confval:: nix_linkcode_resolve
   :type: :code-py:`Callable[[str], str] | None`
   :default: :code-py:`None`

   A function that maps a ``:declaration:`` to an URL.

   For example,
   to map *any* store path to a single GitHub repository:

   .. code-block:: python
      :caption: :file:`conf.py` --- set :code-py:`nix_linkcode_resolve`

      source_repository = "https://github.com/user/repo"

      def nix_linkcode_resolve(path: str) -> str:
          # Strip the nix store and package
          relative_path = "/".join(Path(path).parts[4:])
          return f"{source_repository}/blob/{revision}/{relative_path}"


   If set,
   this uses the :py:mod:`sphinx.ext.linkcode` mechanism to
   add a ``[source]`` link next to the object.

   If :code-py:`None` (the default),
   the declaration path is put as-is in the content of the object.

.. confval:: nix_toc_display_full_path
   :type: :code-py:`bool`
   :default: :code-py:`True`

   Whether to show full names in the table of contents.
