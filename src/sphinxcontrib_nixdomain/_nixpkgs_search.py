"""Searching Nixpkgs for NixOS options and Nix packages."""

# Thanks NH for helping with this implementation!

import importlib.metadata
from collections.abc import Generator
from functools import cache
from typing import Any

from elasticsearch import Elasticsearch

HARDCODED_ES_USER = "aWVSALXpZv"
HARDCODED_ES_PASSWORD = "X8gPHnzL52wFEekuxsfQ9cSh"  # noqa: S105
ES_SERVER = (
    f"https://{HARDCODED_ES_USER}:{HARDCODED_ES_PASSWORD}@search.nixos.org/backend"
)

NIXDOMAIN_VERSION = importlib.metadata.version("sphinxcontrib-nixdomain")
USER_AGENT = f"sphinxcontrib-nixdomain/{NIXDOMAIN_VERSION}"


def _es_client() -> Elasticsearch:
    return Elasticsearch(ES_SERVER)


def _gen_aliases_candidates(aliases: dict[str, Any]) -> Generator[str]:
    for value in aliases.values():
        yield from value["aliases"].keys()


@cache
def _latest_es_index(channel: str) -> str:
    client = _es_client()
    aliases = client.indices.get_alias(name=f"latest-*-{channel}")

    if not aliases:
        raise RuntimeError("failed to fetch latest NixOS Elasticsearch index")

    index = max(_gen_aliases_candidates(aliases))

    if not index:
        raise RuntimeError("failed to fetch latest NixOS Elasticsearch index")

    return index


@cache
def _search_nixpkgs_object(field_name: str, field_value: str, channel: str) -> bool:
    client = _es_client()
    results = client.search(
        index=_latest_es_index(channel),
        body={
            "query": {
                "bool": {
                    "filter": {
                        "term": {field_name: field_value},
                    },
                },
            },
        },
    )

    return bool(
        results["hits"]
        and results["hits"]["hits"]
        and results["hits"]["hits"][0]["_source"],
    )


def search_nixos_option(opt: str, channel: str) -> bool:
    """Check whether a given NixOS option exists in the given Nixpkgs channel."""
    return _search_nixpkgs_object("option_name", opt, channel)


def search_nixpkgs_package(pkg: str, channel: str) -> bool:
    """Check whether a given Nix package exists in the given Nixpkgs channel."""
    return _search_nixpkgs_object("package_attr_name", pkg, channel)
