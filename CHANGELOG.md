# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-01-28

### Changed
- Upgraded MCP SDK from 0.1.0 to 1.26.0 (pinned to v1.x)
- Updated all dependencies to latest stable versions (httpx 0.28.1, aiohttp 3.13.3)
- Updated Python version badge to reflect 3.10–3.13 support

### Added
- Python 3.13 support
- CI testing across Python 3.10, 3.11, 3.12, 3.13
- Package build and validation in CI pipeline
- Security scanning with bandit in CI pipeline

## [0.1.0] - 2025-07-25

### Added
- Initial release of MCP Trilium server
- Full-text search across Trilium notes
- Note management (create, read, update, delete)
- Tree navigation and hierarchical browsing
- Attribute management (labels and relations)
- Recent notes retrieval
- Note export functionality
- Note backup capabilities
- Application info and statistics
- Automatic Claude Desktop configuration generation
- Support for both environment variables and config file setup
- Cross-platform compatibility (Windows, macOS, Linux)
- Comprehensive documentation and FAQ

### Security
- API tokens properly secured and not logged
- Configuration files with sensitive data excluded from git