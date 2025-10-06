"""Target management commands"""

import click
import os
import subprocess
from pathlib import Path
from rich.console import Console
from htb_cli.core.config_manager import ConfigManager

console = Console()


@click.group()
def target():
    """Manage target machine information"""
    pass


@target.command()
@click.argument('machine_name')
@click.argument('ip')
@click.option('--domain', help='Domain name for the target')
def set(machine_name, ip, domain):
    """Set the current target machine"""
    try:
        config_mgr = ConfigManager()
        
        # Save target info
        config_mgr.set('current_target', {
            'name': machine_name,
            'ip': ip,
            'domain': domain if domain else f"{machine_name.lower()}.htb"
        })
        
        console.print(f"\n[green]✓ Target set successfully![/green]")
        console.print(f"Machine: {machine_name}")
        console.print(f"IP: {ip}")
        console.print(f"Domain: {domain if domain else f'{machine_name.lower()}.htb'}\n")
        
        # Create workspace directory for this machine
        workspace = config_mgr.ensure_workspace()
        machine_dir = workspace / machine_name.lower()
        machine_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        for subdir in ['scans', 'exploits', 'loot', 'notes']:
            (machine_dir / subdir).mkdir(exist_ok=True)
        
        console.print(f"[dim]Workspace created: {machine_dir}[/dim]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@target.command()
def show():
    """Show current target information"""
    try:
        config_mgr = ConfigManager()
        target_info = config_mgr.get('current_target')
        
        if not target_info:
            console.print("\n[yellow]No target set[/yellow]")
            console.print("[dim]Use 'htb-cli target set <name> <ip>' to set a target[/dim]\n")
            return
        
        console.print("\n[bold cyan]Current Target[/bold cyan]")
        console.print(f"Machine: {target_info.get('name', 'N/A')}")
        console.print(f"IP: [green]{target_info.get('ip', 'N/A')}[/green]")
        console.print(f"Domain: {target_info.get('domain', 'N/A')}\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@target.command()
@click.option('--shell', type=click.Choice(['bash', 'zsh', 'fish']), default='bash',
              help='Shell type for export')
def export(shell):
    """Export target information as environment variables"""
    try:
        config_mgr = ConfigManager()
        target_info = config_mgr.get('current_target')
        
        if not target_info:
            console.print("[red]✗ No target set[/red]")
            return
        
        ip = target_info.get('ip', '')
        name = target_info.get('name', '')
        domain = target_info.get('domain', '')
        
        console.print("\n[cyan]Environment Variables:[/cyan]\n")
        
        if shell in ['bash', 'zsh']:
            console.print(f"export TARGET_IP={ip}")
            console.print(f"export TARGET_NAME={name}")
            console.print(f"export TARGET_DOMAIN={domain}")
        elif shell == 'fish':
            console.print(f"set -x TARGET_IP {ip}")
            console.print(f"set -x TARGET_NAME {name}")
            console.print(f"set -x TARGET_DOMAIN {domain}")
        
        console.print("\n[dim]Copy and paste the above commands, or run:[/dim]")
        console.print(f"[dim]eval $(htb-cli target export --shell {shell})[/dim]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@target.command()
@click.option('--add', is_flag=True, help='Add entry to /etc/hosts')
@click.option('--remove', is_flag=True, help='Remove entry from /etc/hosts')
def hosts(add, remove):
    """Manage /etc/hosts entries for target"""
    try:
        config_mgr = ConfigManager()
        target_info = config_mgr.get('current_target')
        
        if not target_info:
            console.print("[red]✗ No target set[/red]")
            return
        
        ip = target_info.get('ip', '')
        domain = target_info.get('domain', '')
        
        if add:
            console.print(f"\n[cyan]Adding entry to /etc/hosts...[/cyan]")
            console.print(f"{ip}  {domain}\n")
            
            # Check if entry already exists
            check_cmd = f"grep -q '{domain}' /etc/hosts"
            result = subprocess.run(check_cmd, shell=True)
            
            if result.returncode == 0:
                console.print("[yellow]⚠ Entry already exists in /etc/hosts[/yellow]")
                if not click.confirm("Do you want to update it?"):
                    return
                # Remove old entry first
                subprocess.run(
                    f"sudo sed -i '/{domain}/d' /etc/hosts",
                    shell=True
                )
            
            # Add new entry
            cmd = f"echo '{ip}  {domain}' | sudo tee -a /etc/hosts > /dev/null"
            result = subprocess.run(cmd, shell=True)
            
            if result.returncode == 0:
                console.print("[green]✓ Entry added successfully![/green]\n")
            else:
                console.print("[red]✗ Failed to add entry[/red]\n")
        
        elif remove:
            console.print(f"\n[cyan]Removing entry from /etc/hosts...[/cyan]")
            console.print(f"{domain}\n")
            
            cmd = f"sudo sed -i '/{domain}/d' /etc/hosts"
            result = subprocess.run(cmd, shell=True)
            
            if result.returncode == 0:
                console.print("[green]✓ Entry removed successfully![/green]\n")
            else:
                console.print("[red]✗ Failed to remove entry[/red]\n")
        
        else:
            console.print("\n[yellow]Specify --add or --remove[/yellow]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@target.command()
def workspace():
    """Open target workspace directory"""
    try:
        config_mgr = ConfigManager()
        target_info = config_mgr.get('current_target')
        
        if not target_info:
            console.print("[red]✗ No target set[/red]")
            return
        
        workspace = config_mgr.ensure_workspace()
        machine_dir = workspace / target_info['name'].lower()
        
        if machine_dir.exists():
            console.print(f"\n[cyan]Opening workspace:[/cyan] {machine_dir}\n")
            subprocess.run(f"xdg-open {machine_dir}", shell=True)
        else:
            console.print(f"[yellow]⚠ Workspace directory not found: {machine_dir}[/yellow]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()
