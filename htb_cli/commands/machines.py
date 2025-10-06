"""Machine management commands"""

import click
from rich.console import Console
from rich.table import Table
from htb_cli.core.htb_api import HTBAPIClient, HTBAPIError

console = Console()


@click.group()
def machines():
    """Manage HackTheBox machines"""
    pass


@machines.command()
@click.option('--status', type=click.Choice(['active', 'retired', 'all']), default='active',
              help='Filter by machine status')
@click.option('--os', type=click.Choice(['linux', 'windows', 'all']), default='all',
              help='Filter by operating system')
@click.option('--difficulty', type=click.Choice(['easy', 'medium', 'hard', 'insane', 'all']), 
              default='all', help='Filter by difficulty')
@click.option('--search', help='Search machines by name')
def list(status, os, difficulty, search):
    """List HackTheBox machines"""
    try:
        client = HTBAPIClient()
        console.print("\n[cyan]Fetching machines...[/cyan]\n")
        
        machines = client.get_active_machines()
        
        # Apply filters
        if os != 'all':
            machines = [m for m in machines if m.get('os', '').lower() == os]
        
        if difficulty != 'all':
            machines = [m for m in machines if m.get('difficultyText', '').lower() == difficulty]
        
        if search:
            machines = [m for m in machines if search.lower() in m.get('name', '').lower()]
        
        # Create table
        table = Table(title="HackTheBox Machines")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="bold")
        table.add_column("OS", style="green")
        table.add_column("Difficulty", style="yellow")
        table.add_column("Rating", style="magenta")
        table.add_column("User Owns", style="blue")
        table.add_column("Root Owns", style="red")
        
        for machine in machines:
            diff_text = machine.get('difficultyText', 'N/A')
            diff_color = {
                'Easy': 'green',
                'Medium': 'yellow', 
                'Hard': 'red',
                'Insane': 'bright_red'
            }.get(diff_text, 'white')
            
            table.add_row(
                str(machine.get('id', 'N/A')),
                machine.get('name', 'N/A'),
                machine.get('os', 'N/A'),
                f"[{diff_color}]{diff_text}[/{diff_color}]",
                str(machine.get('star', 'N/A')),
                str(machine.get('user_owns_count', 'N/A')),
                str(machine.get('root_owns_count', 'N/A'))
            )
        
        console.print(table)
        console.print(f"\n[dim]Total machines: {len(machines)}[/dim]\n")
        
    except HTBAPIError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@machines.command()
@click.argument('machine_name')
def info(machine_name):
    """Get detailed information about a machine"""
    try:
        client = HTBAPIClient()
        console.print(f"\n[cyan]Fetching information for '{machine_name}'...[/cyan]\n")
        
        # Find machine by name
        machines_list = client.get_active_machines()
        machine = next((m for m in machines_list if m['name'].lower() == machine_name.lower()), None)
        
        if not machine:
            console.print(f"[red]✗ Machine '{machine_name}' not found[/red]")
            return
        
        # Get detailed info
        details = client.get_machine_info(machine['id'])
        info = details.get('info', {})
        
        console.print(f"[bold cyan]Machine: {info.get('name', 'N/A')}[/bold cyan]")
        console.print(f"[dim]ID: {info.get('id', 'N/A')}[/dim]\n")
        console.print(f"OS: {info.get('os', 'N/A')}")
        console.print(f"Difficulty: {info.get('difficultyText', 'N/A')}")
        console.print(f"Rating: {info.get('stars', 'N/A')}/5.0")
        console.print(f"Points: {info.get('points', 'N/A')}")
        console.print(f"Release Date: {info.get('release', 'N/A')}")
        console.print(f"\nUser Owns: {info.get('user_owns_count', 'N/A')}")
        console.print(f"Root Owns: {info.get('root_owns_count', 'N/A')}")
        
        if info.get('ip'):
            console.print(f"\n[green]IP Address: {info['ip']}[/green]")
        
        console.print()
        
    except HTBAPIError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@machines.command()
@click.argument('machine_name')
def start(machine_name):
    """Start/spawn a machine"""
    try:
        client = HTBAPIClient()
        
        # Find machine by name
        machines_list = client.get_active_machines()
        machine = next((m for m in machines_list if m['name'].lower() == machine_name.lower()), None)
        
        if not machine:
            console.print(f"[red]✗ Machine '{machine_name}' not found[/red]")
            return
        
        console.print(f"\n[cyan]Starting machine '{machine_name}'...[/cyan]\n")
        result = client.start_machine(machine['id'])
        
        console.print(f"[green]✓ Machine started successfully![/green]")
        console.print(f"IP Address: [bold]{result.get('ip', 'N/A')}[/bold]\n")
        
    except HTBAPIError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@machines.command()
def stop():
    """Stop the currently running machine"""
    try:
        client = HTBAPIClient()
        console.print("\n[cyan]Stopping machine...[/cyan]\n")
        
        client.stop_machine()
        console.print("[green]✓ Machine stopped successfully![/green]\n")
        
    except HTBAPIError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@machines.command()
def active():
    """Show currently active/spawned machine"""
    try:
        client = HTBAPIClient()
        active_machine = client.get_active_machine()
        
        if not active_machine:
            console.print("\n[yellow]No active machine[/yellow]\n")
            return
        
        console.print(f"\n[bold cyan]Active Machine[/bold cyan]")
        console.print(f"Name: {active_machine.get('name', 'N/A')}")
        console.print(f"IP: [green]{active_machine.get('ip', 'N/A')}[/green]")
        console.print(f"OS: {active_machine.get('os', 'N/A')}")
        console.print(f"Difficulty: {active_machine.get('difficulty', 'N/A')}\n")
        
    except HTBAPIError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@machines.command()
@click.argument('machine_name')
@click.argument('flag')
@click.option('--user', is_flag=True, help='Submit user flag')
@click.option('--root', is_flag=True, help='Submit root flag')
def submit(machine_name, flag, user, root):
    """Submit a flag for a machine"""
    try:
        client = HTBAPIClient()
        
        # Find machine by name
        machines_list = client.get_active_machines()
        machine = next((m for m in machines_list if m['name'].lower() == machine_name.lower()), None)
        
        if not machine:
            console.print(f"[red]✗ Machine '{machine_name}' not found[/red]")
            return
        
        # Determine difficulty (user=10, root=20)
        difficulty = 10 if user else (20 if root else 10)
        
        console.print(f"\n[cyan]Submitting flag...[/cyan]\n")
        result = client.submit_flag(machine['id'], flag, difficulty)
        
        if result.get('success'):
            console.print("[green]✓ Correct flag! Well done![/green]\n")
        else:
            console.print("[red]✗ Incorrect flag[/red]\n")
        
    except HTBAPIError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()
