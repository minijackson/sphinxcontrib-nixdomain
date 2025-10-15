from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar

from sphinx.domains import Domain, ObjType
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.nodes import make_refnode

from ._library_autodoc import NixAutoFunctionDirective, NixAutoLibraryDirective
from ._module_autodoc import NixAutoModuleDirective, NixAutoOptionDirective
from ._package_autodoc import NixAutoPackageDirective, NixAutoPackagesDirective
from ._utils import EntityType, option_lt, split_attr_path
from .library import FunctionDirective, LibraryIndex
from .module import OptionDirective, OptionsIndex
from .package import PackageDirective

if TYPE_CHECKING:
    from collections.abc import Generator

    from docutils.nodes import Element
    from sphinx.addnodes import pending_xref
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment


logger = logging.getLogger(__name__)

# TODO: add options to the future autodoc:
# - flat: choose whether the options are displayed flat or nested
# - show_prefix: if options are displayed nested,
#   choose whether the option prefix is repeated

object_data = tuple[str, str, str, str, str, int]


@dataclass
class RefEntity:
    """A referenceable Nix entity.

    This can be for example a function, package, or an option.

    This dataclass is used to figure out the entity's info
    when a reference is resolved.
    """

    name: str
    path: str
    typ: EntityType
    docname: str
    anchor: str
    priority: int

    def to_tuple(self) -> tuple[str, str, str, str, str, int]:
        """Get this entity as tuple, as needed by Sphinx."""
        # name, dispname, type, docname, anchor, priority
        return (
            self.name,
            self.path,
            self.typ.directive_name(),
            self.docname,
            self.anchor,
            self.priority,
        )

    def __lt__(self, other: RefEntity) -> bool:
        if self.typ == EntityType.OPTION:
            # Sort .enable options first
            return option_lt(self.path, other.path)

        return self.path < other.path


T = TypeVar("T")


def _last(li: list[T], default: T = None) -> T:
    return next(iter(li[-1:]), default)


class NixXRefRole(XRefRole):
    def process_link(
        self,
        env: BuildEnvironment,
        refnode: Element,
        has_explicit_title: bool,
        title: str,
        target: str,
    ) -> tuple[str, str]:
        refnode["nix:option"] = _last(env.ref_context.get("nix:option", []), "")
        refnode["nix:function"] = _last(env.ref_context.get("nix:function", []), "")
        return super().process_link(env, refnode, has_explicit_title, title, target)


class NixDomain(Domain):
    name = "nix"
    label = "Nix"

    object_types: dict[str, ObjType] = {  # noqa: RUF012
        "option": ObjType("option", "option", "obj"),
        "function": ObjType("function", "func", "bind", "obj"),
        "package": ObjType("package", "pkg", "bind", "obj"),
    }

    roles = {  # noqa: RUF012
        "bind": NixXRefRole(warn_dangling=True),
        "func": NixXRefRole(warn_dangling=True),
        "option": NixXRefRole(warn_dangling=True),
        "pkg": NixXRefRole(warn_dangling=True),
        "obj": NixXRefRole(warn_dangling=True),
    }
    directives = {  # noqa: RUF012
        "autolibrary": NixAutoLibraryDirective,
        "autofunction": NixAutoFunctionDirective,
        "automodule": NixAutoModuleDirective,
        "autooption": NixAutoOptionDirective,
        "autopackage": NixAutoPackageDirective,
        "autopackages": NixAutoPackagesDirective,
        "function": FunctionDirective,
        "option": OptionDirective,
        "package": PackageDirective,
    }
    indices = [  # noqa: RUF012
        LibraryIndex,
        OptionsIndex,
    ]
    initial_data = {  # noqa: RUF012
        "functions": [],
        "options": [],
        "packages": [],
    }
    data_version = 0

    def get_functions(self) -> Generator[RefEntity]:
        """Get all functions in this domain."""
        yield from self.data["functions"]

    def get_options(self) -> Generator[RefEntity]:
        """Get all options in this domain."""
        yield from self.data["options"]

    def get_packages(self) -> Generator[RefEntity]:
        """Get all options in this domain."""
        yield from self.data["packages"]

    def get_entities(self) -> Generator[RefEntity]:
        """Get all entities in this domain."""
        yield from self.get_options()
        yield from self.get_packages()
        yield from self.get_functions()

    def get_objects(self) -> Generator[object_data]:
        """Get all entities in this domain.

        Returns a tuple, as needed by Sphinx.
        """
        for entity in self.get_entities():
            yield entity.to_tuple()

    def resolve_any_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: pending_xref,
        contnode: Element,
    ) -> list[tuple[str, Element]]:
        results: list[tuple[str, Element]] = []
        for objtype in self.object_types:
            result = self.resolve_xref(
                env,
                fromdocname,
                builder,
                objtype,
                target,
                node,
                contnode,
            )
            if result:
                results.append((f"nix:{self.role_for_objtype(objtype)}", result))
        return results

    def resolve_xref(
        self,
        _env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        typ: str,
        target: str,
        node: pending_xref,
        contnode: Element,
    ) -> Element | None:
        """Resolve the pending_xref node with the given typ and target."""
        objtypes = self.objtypes_for_role(typ)

        if not objtypes:
            return None

        for objtype in objtypes:
            if res := self._resolve_single_type_xref(
                fromdocname,
                builder,
                objtype,
                target,
                node,
                contnode,
            ):
                return res

        return None

    def _resolve_single_type_xref(
        self,
        fromdocname: str,
        builder: Builder,
        objtype: str,
        target: str,
        node: pending_xref,
        contnode: Element,
    ) -> Element | None:
        object_getter = None
        if objtype == "function":
            context_path = split_attr_path(node.get("nix:function", ""))
            object_getter = self.get_functions
        elif objtype == "option":
            context_path = split_attr_path(node.get("nix:option", ""))
            object_getter = self.get_options
        elif objtype == "package":
            context_path = split_attr_path(node.get("nix:package", ""))
            object_getter = self.get_packages
        else:
            logger.warning("Unknown Nix object type: %s", objtype, location=node)
            return None

        target_path = split_attr_path(target)

        # Make a list of possible referred attributes,
        # depending on the context
        candidates = [
            ".".join(context_path[:prefix_len] + target_path)
            for prefix_len in range(len(context_path) + 1)
        ]
        # Order candidates by most nested attribute first
        candidates.reverse()

        matches = [entity for entity in object_getter() if entity.path in candidates]
        # Sort matches according to the candidates list
        matches.sort(key=lambda entity: candidates.index(entity.path))

        if len(matches) > 0:
            entity = matches[0]
            return make_refnode(
                builder,
                fromdocname,
                entity.docname,
                entity.anchor,
                contnode,
                f"{entity.typ} {entity.path}",
            )

        return None

    def add_function(
        self,
        path: str,
        _arguments: dict[str, str],
    ) -> None:
        """Add a new function to the domain."""
        anchor = f"nix-function-{path}"

        self.data["functions"].append(
            RefEntity(path, path, EntityType.FUNCTION, self.env.docname, anchor, 0),
        )

    def add_option(self, path: str, _options: dict[str, str]) -> None:
        """Add a new module option to the domain."""
        anchor = f"nix-option-{path}"

        self.data["options"].append(
            RefEntity(path, path, EntityType.OPTION, self.env.docname, anchor, 0),
        )

    def add_package(self, path: str, _options: dict[str, str]) -> None:
        """Add a new module option to the domain."""
        anchor = f"nix-package-{path}"

        self.data["packages"].append(
            RefEntity(path, path, EntityType.PACKAGE, self.env.docname, anchor, 0),
        )
