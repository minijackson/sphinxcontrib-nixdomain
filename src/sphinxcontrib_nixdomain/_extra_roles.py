from docutils import nodes
from docutils.nodes import Node, system_message
from sphinx.util import encode_uri
from sphinx.util.docutils import ReferenceRole

from ._nixpkgs_search import search_nixos_option, search_nixpkgs_package


class NixpkgsPkg(ReferenceRole):
    """Link to a Nix package defined in Nixpkgs."""

    def run(self) -> tuple[list[Node], list[system_message]]:
        reference = nodes.reference(
            "",
            "",
            internal=False,
            refuri=f"https://search.nixos.org/packages?query={encode_uri(self.target)}",
            reftitle=f"Nixpkgs package {self.target}",
        )

        reference += nodes.literal(
            self.title,
            self.title,
            classes=["nix", "nix-nixpkgs-pkg"],
        )

        system_messages = []
        if not search_nixpkgs_package(
            self.target,
            self.config.nixdomain_default_channel,
        ):
            system_messages.append(
                self.inliner.reporter.error(
                    f"couldn't find package {self.target} in Nixpkgs",
                ),
            )

        return [reference], system_messages


class NixosOption(ReferenceRole):
    """Link to a NixOS option defined in Nixpkgs."""

    def run(self) -> tuple[list[Node], list[system_message]]:
        reference = nodes.reference(
            "",
            "",
            internal=False,
            refuri=f"https://search.nixos.org/options?query={encode_uri(self.target)}",
            reftitle=f"NixOS option {self.target}",
        )

        reference += nodes.literal(
            self.title,
            self.title,
            classes=["nix", "nix-nixos-option"],
        )

        system_messages = []
        # TODO: catch exceptions
        if not search_nixos_option(
            self.target,
            self.config.nixdomain_default_channel,
        ):
            system_messages.append(
                self.inliner.reporter.error(
                    f"couldn't find package {self.target} in Nixpkgs",
                ),
            )

        return [reference], system_messages
