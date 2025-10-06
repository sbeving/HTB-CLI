#!/usr/bin/env python3
"""
HTB-CLI - HackTheBox Command Line Utility
Main entry point for the CLI application
"""

import click
from rich.console import Console
from htb_cli.commands import machines, vpn, target, scan, config, notes

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """HTB-CLI - HackTheBox Command Line Utility
    
    Automate your HackTheBox workflow with machine management,
    VPN handling, scanning, and exploitation tools.
    """
    pass


# Register command groups
cli.add_command(config.config)
cli.add_command(machines.machines)
cli.add_command(vpn.vpn)
cli.add_command(target.target)
cli.add_command(scan.scan)
cli.add_command(notes.notes)


@cli.command()
def init():
    """Initialize HTB-CLI configuration"""
    from htb_cli.core.config_manager import ConfigManager
    
    console.print("\n[bold cyan]🚀 Initializing HTB-CLI...[/bold cyan]\n")
    
    config_mgr = ConfigManager()
    
    if config_mgr.config_exists():
        console.print("[yellow]⚠️  Configuration already exists![/yellow]")
        if not click.confirm("Do you want to reconfigure?"):
            return
    
    # Get API token
    console.print("[bold]Step 1:[/bold] HTB API Token")
    console.print("Get your token from: https://app.hackthebox.com/profile/settings")
    api_token = click.prompt("Enter your HTB API token", hide_input=True)
    
    # Get workspace directory
    console.print("\n[bold]Step 2:[/bold] Workspace Directory")
    workspace = click.prompt("Enter your HTB workspace directory", 
                            default="~/htb")
    
    # Get default VPN server
    console.print("\n[bold]Step 3:[/bold] Default VPN Server")
    console.print("Examples: us-vip-1, eu-vip-1, au-vip-1")
    vpn_server = click.prompt("Enter default VPN server", default="us-vip-1")
    
    # Save configuration
    config_mgr.save_config({
        "api_token": api_token,
        "workspace": workspace,
        "vpn": {
            "default_server": vpn_server,
            "auto_connect": False
        },
        "scan": {
            "default_threads": "1000",
            "save_results": True
        }
    })
    
    console.print("\n[bold green]✓ Configuration saved successfully![/bold green]")
    console.print(f"[dim]Config file: {config_mgr.config_file}[/dim]\n")
    console.print("[cyan]Run 'htb-cli machines list' to get started![/cyan]\n")


if __name__ == "__main__":
    cli()
