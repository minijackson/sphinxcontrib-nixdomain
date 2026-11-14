from docutils import nodes
from docutils.nodes import Node, system_message
from sphinx.util import encode_uri
from sphinx.util.docutils import ReferenceRole


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

        # TODO: return an error if the option isn't found in Nixpkgs
        return [reference], []


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

        # TODO: return an error if the option isn't found in NixOS
        return [reference], []
