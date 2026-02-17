# Changelog

All notable changes of **RCIAM Federation Registry Agent** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

RCIAM Federation Registry Agent synchronizes data between RCIAM Federation Registry and IAM solutions such as Keycloak, SATOSA, SimpleSAMLphp and MITREid Connect.

The main standalone deployment scripts are located under `bin/`:

- `deployer_keycloak`
- `deployer_mitreid`
- `deployer_ssp`

---

## [4.0.0] - 2026-02-13

### Added

- Support for **Keycloak v26+ token exchange configuration** using the new client attribute:
  - `standard.token.exchange.enabled=true`
