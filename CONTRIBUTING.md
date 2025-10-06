# Contributing to HTB-CLI

Thank you for considering contributing to HTB-CLI! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/HTB-CLI.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -am 'Add some feature'`
7. Push to the branch: `git push origin feature/your-feature-name`
8. Submit a pull request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/HTB-CLI.git
cd HTB-CLI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy
```

## Code Style

We follow PEP 8 guidelines for Python code:

- Use 4 spaces for indentation
- Line length maximum: 100 characters
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Type hints are encouraged

Format your code with Black:
```bash
black htb_cli/
```

Check with flake8:
```bash
flake8 htb_cli/
```

## Project Structure

```
HTB-CLI/
├── htb_cli/
│   ├── __init__.py
│   ├── main.py              # Main CLI entry point
│   ├── core/                # Core functionality
│   │   ├── config_manager.py
│   │   └── htb_api.py
│   ├── commands/            # CLI command modules
│   │   ├── machines.py
│   │   ├── vpn.py
│   │   ├── target.py
│   │   ├── scan.py
│   │   ├── notes.py
│   │   ├── exploit.py
│   │   └── config.py
│   └── utils.py             # Utility functions
├── tests/                   # Test files
├── examples/                # Example scripts
├── docs/                    # Additional documentation
└── setup.py                 # Package setup
```

## Adding a New Command

1. Create a new file in `htb_cli/commands/` or add to existing file
2. Use the Click framework for CLI commands
3. Follow this template:

```python
import click
from rich.console import Console

console = Console()

@click.group()
def mycommand():
    """Description of your command group"""
    pass

@mycommand.command()
@click.option('--option', help='Description')
@click.argument('argument')
def subcommand(option, argument):
    """Description of your subcommand"""
    try:
        # Your implementation here
        console.print("[green]Success![/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()
```

4. Register the command in `htb_cli/main.py`:

```python
from htb_cli.commands import mycommand

cli.add_command(mycommand.mycommand)
```

## Adding API Endpoints

Add new API methods to `htb_cli/core/htb_api.py`:

```python
def new_api_method(self, param: str) -> Dict[str, Any]:
    """Description of what this method does"""
    return self._request("GET", f"endpoint/{param}")
```

## Testing

Write tests for new features:

```python
# tests/test_feature.py
import pytest
from htb_cli.core.config_manager import ConfigManager

def test_config_manager():
    config = ConfigManager()
    config.set('test_key', 'test_value')
    assert config.get('test_key') == 'test_value'
```

Run tests:
```bash
pytest tests/
```

## Documentation

- Update README.md if you add major features
- Update USAGE.md with examples of new commands
- Add docstrings to all new functions and classes
- Update ROADMAP.md if implementing planned features

## Pull Request Guidelines

1. **Title**: Use descriptive titles (e.g., "Add SMB enumeration command")
2. **Description**: Explain what changes you made and why
3. **Testing**: Describe how you tested your changes
4. **Breaking Changes**: Note any breaking changes
5. **Documentation**: Update relevant documentation

Example PR description:
```
## Changes
- Added SMB enumeration command
- Integrated with smbclient and enum4linux
- Added automatic null session testing

## Testing
- Tested against Windows machines
- Verified output formatting
- Checked error handling

## Documentation
- Updated USAGE.md with examples
- Added docstrings to new functions
```

## Bug Reports

When filing bug reports, include:

1. HTB-CLI version: `htb-cli --version`
2. Python version: `python3 --version`
3. Operating system
4. Steps to reproduce
5. Expected behavior
6. Actual behavior
7. Error messages (full traceback)
8. Relevant configuration (with sensitive data removed)

## Feature Requests

For feature requests, provide:

1. Clear description of the feature
2. Use case / motivation
3. Example usage (pseudocode or CLI commands)
4. Any relevant references or similar tools

## Security Issues

If you discover a security vulnerability, please email the maintainer directly instead of opening a public issue.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive criticism
- Respect differing viewpoints

## Questions?

- Open an issue for general questions
- Check existing issues before creating new ones
- Tag issues appropriately (bug, enhancement, question, etc.)

## License

By contributing to HTB-CLI, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to HTB-CLI! 🎉
