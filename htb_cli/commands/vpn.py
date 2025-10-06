"""VPN management commands"""

import click
import subprocess
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from htb_cli.core.htb_api import HTBAPIClient, HTBAPIError
from htb_cli.core.config_manager import ConfigManager

console = Console()


@click.group()
def vpn():
    """Manage HackTheBox VPN connections"""
    pass


@vpn.command()
def servers():
    """List available VPN servers"""
    try:
        client = HTBAPIClient()
        console.print("\n[cyan]Fetching VPN servers...[/cyan]\n")
        
        servers_list = client.get_vpn_servers()
        
        table = Table(title="Available VPN Servers")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="bold")
        table.add_column("Location", style="green")
        table.add_column("Type", style="yellow")
        
        for server in servers_list:
            table.add_row(
                str(server.get('id', 'N/A')),
                server.get('friendly_name', 'N/A'),
                server.get('location', 'N/A'),
                server.get('type', 'N/A')
            )
        
        console.print(table)
        console.print()
        
    except HTBAPIError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@vpn.command()
@click.option('--server', help='VPN server name (e.g., us-vip-1)')
@click.option('--output', type=click.Path(), help='Output path for VPN config')
def download(server, output):
    """Download VPN configuration file"""
    try:
        client = HTBAPIClient()
        config_mgr = ConfigManager()
        
        if not server:
            server = config_mgr.get('vpn.default_server', 'us-vip-1')
        
        console.print(f"\n[cyan]Downloading VPN config for '{server}'...[/cyan]\n")
        
        # Get server list to find ID
        servers_list = client.get_vpn_servers()
        server_info = next(
            (s for s in servers_list if server.lower() in s.get('friendly_name', '').lower()),
            None
        )
        
        if not server_info:
            console.print(f"[red]✗ Server '{server}' not found[/red]")
            console.print("[dim]Run 'htb-cli vpn servers' to see available servers[/dim]\n")
            return
        
        # Download VPN config
        vpn_config = client.download_vpn_config(server_info['id'])
        
        # Determine output path
        if not output:
            config_dir = config_mgr.config_dir / "vpn"
            config_dir.mkdir(exist_ok=True)
            output = config_dir / f"htb-{server}.ovpn"
        
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(vpn_config)
        
        console.print(f"[green]✓ VPN config downloaded successfully![/green]")
        console.print(f"Location: {output_path}\n")
        
        # Save to config for easy connection
        config_mgr.set('vpn.current_config', str(output_path))
        
    except HTBAPIError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@vpn.command()
@click.option('--config', type=click.Path(exists=True), help='Path to VPN config file')
def connect(config):
    """Connect to HackTheBox VPN"""
    try:
        config_mgr = ConfigManager()
        
        if not config:
            config = config_mgr.get('vpn.current_config')
            if not config or not Path(config).exists():
                console.print("[red]✗ No VPN config found[/red]")
                console.print("[dim]Download a config first: htb-cli vpn download[/dim]\n")
                return
        
        console.print(f"\n[cyan]Connecting to VPN...[/cyan]")
        console.print(f"[dim]Config: {config}[/dim]\n")
        console.print("[yellow]Note: You may need to enter your password for sudo[/yellow]\n")
        
        # Connect using openvpn
        cmd = f"sudo openvpn --config {config} --daemon"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            console.print("[green]✓ VPN connection initiated![/green]")
            console.print("[dim]Run 'htb-cli vpn status' to check connection status[/dim]\n")
        else:
            console.print(f"[red]✗ Failed to connect: {result.stderr}[/red]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@vpn.command()
def disconnect():
    """Disconnect from HackTheBox VPN"""
    try:
        console.print("\n[cyan]Disconnecting VPN...[/cyan]\n")
        
        # Kill openvpn process
        cmd = "sudo killall openvpn"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            console.print("[green]✓ VPN disconnected successfully![/green]\n")
        else:
            console.print("[yellow]⚠ No active VPN connection found[/yellow]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@vpn.command()
def status():
    """Check VPN connection status"""
    try:
        console.print("\n[cyan]Checking VPN status...[/cyan]\n")
        
        # Check if openvpn is running
        result = subprocess.run(
            "ps aux | grep '[o]penvpn'",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            console.print("[green]✓ VPN is connected[/green]")
            
            # Try to get tun0 IP
            ip_result = subprocess.run(
                "ip addr show tun0 2>/dev/null | grep 'inet ' | awk '{print $2}'",
                shell=True,
                capture_output=True,
                text=True
            )
            
            if ip_result.stdout.strip():
                console.print(f"IP Address: {ip_result.stdout.strip()}")
            
            console.print()
        else:
            console.print("[yellow]✗ VPN is not connected[/yellow]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()
