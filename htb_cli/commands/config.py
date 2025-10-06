"""Configuration commands"""

import click
from rich.console import Console
from rich.table import Table
from htb_cli.core.config_manager import ConfigManager

console = Console()


@click.group()
def config():
    """Manage HTB-CLI configuration"""
    pass


@config.command()
@click.argument('key')
@click.argument('value')
def set(key, value):
    """Set a configuration value"""
    try:
        config_mgr = ConfigManager()
        config_mgr.set(key, value)
        
        console.print(f"\n[green]✓ Configuration updated![/green]")
        console.print(f"{key} = {value}\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@config.command()
@click.argument('key')
def get(key):
    """Get a configuration value"""
    try:
        config_mgr = ConfigManager()
        value = config_mgr.get(key)
        
        if value is not None:
            console.print(f"\n{key} = {value}\n")
        else:
            console.print(f"\n[yellow]Key '{key}' not found[/yellow]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@config.command()
def show():
    """Show all configuration"""
    try:
        config_mgr = ConfigManager()
        cfg = config_mgr.load_config()
        
        if not cfg:
            console.print("\n[yellow]No configuration found[/yellow]")
            console.print("[dim]Run 'htb-cli init' to initialize[/dim]\n")
            return
        
        console.print("\n[bold cyan]HTB-CLI Configuration[/bold cyan]\n")
        
        # Display config in a nice format
        def print_dict(d, indent=0):
            for key, value in d.items():
                if isinstance(value, dict):
                    console.print("  " * indent + f"[cyan]{key}:[/cyan]")
                    print_dict(value, indent + 1)
                else:
                    # Mask sensitive data
                    if 'token' in key.lower() or 'password' in key.lower():
                        value = '*' * 20
                    console.print("  " * indent + f"[cyan]{key}:[/cyan] {value}")
        
        print_dict(cfg)
        console.print(f"\n[dim]Config file: {config_mgr.config_file}[/dim]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@config.command()
@click.argument('token')
def set_token(token):
    """Set HTB API token"""
    try:
        config_mgr = ConfigManager()
        config_mgr.set('api_token', token)
        
        console.print("\n[green]✓ API token updated successfully![/green]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@config.command()
def path():
    """Show configuration file path"""
    try:
        config_mgr = ConfigManager()
        console.print(f"\n{config_mgr.config_file}\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()
