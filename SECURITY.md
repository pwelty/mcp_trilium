# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in MCP Trilium, please report it responsibly:

### How to Report

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. Send an email to: [paul.welty@example.com] (replace with your actual email)
3. Include detailed information about the vulnerability
4. Provide steps to reproduce if possible

### What to Include

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Any suggested fixes (if you have them)

### Response Timeline

- **Initial Response**: Within 48 hours of report
- **Status Updates**: Weekly updates on investigation progress
- **Resolution**: Security fixes will be prioritized and released as soon as possible

## Security Considerations

### API Token Security

- **Never commit API tokens** to version control
- Store tokens in environment variables or secure configuration files
- API tokens are not logged by this application
- Rotate tokens regularly in your Trilium instance

### Network Security

- The MCP server connects directly to your Trilium instance
- No data is sent to external services (except your Trilium server)
- All communication uses HTTPS when connecting to remote Trilium instances
- Local connections may use HTTP if your Trilium instance is configured that way

### Data Privacy

- Your notes and data remain on your local machine and Trilium server
- The MCP server only accesses data when explicitly requested through Claude Desktop
- No analytics or telemetry data is collected
- Configuration files containing sensitive data are excluded from git tracking

### Best Practices

1. **Use HTTPS** for remote Trilium connections
2. **Limit API token permissions** in Trilium to only what's needed
3. **Keep your Trilium instance updated** with security patches
4. **Use strong authentication** for your Trilium instance
5. **Monitor access logs** in your Trilium instance if needed

## Acknowledgments

We appreciate security researchers and users who report vulnerabilities responsibly.

## Disclosure Policy

- Security fixes will be released as soon as possible
- CVE numbers will be requested for significant vulnerabilities
- Public disclosure will happen after fixes are available
- Credit will be given to security researchers who report issues responsibly