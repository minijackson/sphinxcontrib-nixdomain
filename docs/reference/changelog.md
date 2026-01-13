# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

  [Unreleased]: https://github.com/minijackson/sphinxcontrib-nixdomain/compare/v0.1.2...main

## [0.1.2] --- 2026-01-12

### Changed

- All documentation URLs now point to the ReadTheDocs documentation website.

  [0.1.2]: https://github.com/minijackson/sphinxcontrib-nixdomain/compare/v0.1.1...v0.1.2

## [0.1.1] --- 2026-01-12

### Added

- Set up [`flake-compat`] to allow for non-flake usage.
- Allow documenting all modules in the {rst:dir}`nix:automodule` directive.
- Set up a ReadTheDocs build of the documentation

  [`flake-compat`]: https://github.com/NixOS/flake-compat
  [0.1.1]: https://github.com/minijackson/sphinxcontrib-nixdomain/compare/v0.1.0...v0.1.1

## [0.1.0] --- 2026-01-08

First release!

### Added

Everything!

Support for:

- NixOS options
- Nix packages
- Nix libraries

Generates an index for options and libraries.

Has support for resolving source links
by using the {confval}`nixdomain_linkcode_resolve` configuration.

  [0.1.0]: https://github.com/minijackson/sphinxcontrib-nixdomain/releases/tag/v0.1.0
