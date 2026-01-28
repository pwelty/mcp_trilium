# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Updated MCP SDK from 0.1.0 to 1.26.0 (pinned to v1.x)
- Updated all dependencies to latest versions
- Added Python 3.13 support and CI testing
- Updated Python version badge to reflect 3.10-3.13 support

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

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- API tokens properly secured and not logged
- Configuration files with sensitive data excluded from git


---

## Release Notes Template

When releasing a new version, copy this template:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features added in this release

### Changed  
- Changes to existing functionality

### Deprecated
- Features that will be removed in future versions

### Removed
- Features removed in this release

### Fixed
- Bug fixes

### Security
- Security improvements or fixes
```