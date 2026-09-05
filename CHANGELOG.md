# Changelog

All notable changes to this module are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Fixed

- Forward client-provided `x-amz-content-sha256` through the existing signed Lambda origin request header allowlist. Lambda OAC remains configured for `always` signing with `sigv4`; authentication and the rest of the policy are unchanged.
- Clients sending request bodies (for example, POST/PUT) must supply `x-amz-content-sha256` as the hexadecimal SHA-256 digest of the exact body bytes sent. Hash the final serialized body, not a separately serialized object; whitespace, encoding, or other body changes invalidate the hash. This module only forwards the header and does not calculate it or make unsigned payloads valid.

### Added

- Credential-free Python standard-library source regression checks for the signed Lambda header allowlist and OAC configuration. These are not Terraform plan or deployed integration tests.

## [0.2.2] - 2026-09-05

### Added

- terraform-docs-generated interface documentation in README (Requirements/Providers/Inputs/Outputs) with a CI drift check.

## [0.2.1] - 2026-09-05

### Added

- CHANGELOG.md.

## [0.2.0] - 2026-09-04

### Added

- CI workflow for Terraform validation and release workflow for tagged releases.
- `.tflint.hcl` linting configuration.
- MIT LICENSE.
- README badges for CI status and Terraform Registry.

### Changed

- AWS provider version constraint to `>= 5.0, < 7.0`.
- Updated `.terraform.lock.hcl`.

> Historical releases are documented in [GitHub Releases](https://github.com/pomo-studio/terraform-aws-ssr-cloudfront-support/releases).
