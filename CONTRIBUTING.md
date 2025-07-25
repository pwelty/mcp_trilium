# Contributing to MCP Trilium

Thank you for your interest in contributing to MCP Trilium! This project welcomes contributions from the community.

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker to report bugs or request features
- Check existing issues first to avoid duplicates
- Provide clear reproduction steps for bugs
- Include relevant system information (OS, Python version, Trilium version)

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/mcp-trilium.git
   cd mcp-trilium
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Copy and configure the config template:
   ```bash
   cp config.json.template config.json
   # Edit config.json with your Trilium instance details
   ```

### Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the coding standards below
3. Test your changes thoroughly
4. Commit with clear, descriptive messages
5. Push to your fork and create a pull request

### Coding Standards

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to new functions and classes
- Keep functions focused and concise
- Handle errors gracefully with appropriate exception handling

### Testing

- Test your changes against a real Trilium instance
- Verify the MCP server works with Claude Desktop
- Test error conditions and edge cases
- Update documentation if needed

### Pull Request Process

1. Ensure your PR has a clear title and description
2. Reference any related issues
3. Update the README if you've added new features
4. Ensure your code follows the project's coding standards
5. Be responsive to feedback during the review process

## Architecture

### Project Structure

- `main.py` - MCP server entry point and tool definitions
- `services/trilium.py` - Trilium API client and business logic
- `config.json.template` - Configuration template
- `requirements.txt` - Python dependencies

### Adding New Features

1. Add new methods to the `TriliumService` class in `services/trilium.py`
2. Add corresponding MCP tools in `main.py`
3. Update the README with documentation for new tools
4. Test the new functionality end-to-end

## Code of Conduct

This project follows a simple code of conduct:

- Be respectful and professional in all interactions
- Focus on constructive feedback and collaboration
- Help maintain a welcoming environment for all contributors

## Questions?

Feel free to open an issue for questions about contributing or join discussions in existing issues.