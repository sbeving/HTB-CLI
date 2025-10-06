"""Notes and documentation commands"""

import click
import subprocess
from datetime import datetime
from pathlib import Path
from rich.console import Console
from htb_cli.core.config_manager import ConfigManager

console = Console()


@click.group()
def notes():
    """Manage machine notes and writeups"""
    pass


@notes.command()
@click.option('--machine', help='Machine name (uses current target if not specified)')
def create(machine):
    """Create a new notes file for a machine"""
    try:
        config_mgr = ConfigManager()
        
        if not machine:
            target_info = config_mgr.get('current_target')
            if not target_info:
                console.print("[red]✗ No machine specified and no current target set[/red]")
                return
            machine = target_info.get('name')
            ip = target_info.get('ip')
            domain = target_info.get('domain')
        else:
            ip = 'N/A'
            domain = f'{machine.lower()}.htb'
        
        workspace = config_mgr.ensure_workspace()
        notes_dir = workspace / machine.lower() / 'notes'
        notes_dir.mkdir(parents=True, exist_ok=True)
        
        notes_file = notes_dir / f'{machine.lower()}_notes.md'
        
        if notes_file.exists():
            console.print(f"[yellow]⚠ Notes file already exists: {notes_file}[/yellow]")
            if not click.confirm("Do you want to open it?"):
                return
        else:
            # Create template
            template = f"""# {machine} - HTB Machine Notes

**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**IP:** {ip}  
**Domain:** {domain}  
**OS:** TBD  
**Difficulty:** TBD

---

## Enumeration

### Port Scan
```bash
# Quick scan
htb-cli scan quick

# Full scan
htb-cli scan full
```

**Open Ports:**
- 

### Web Enumeration
```bash
htb-cli scan web http://{ip}
```

**Findings:**
- 

---

## Exploitation

### Initial Access

**Vulnerability:**

**Exploit:**
```bash

```

**User Flag:**
```

```

---

## Privilege Escalation

**Method:**

**Exploit:**
```bash

```

**Root Flag:**
```

```

---

## Tools Used
- nmap
- gobuster
- 

---

## References
- 

---

## Notes
- 
"""
            notes_file.write_text(template)
            console.print(f"\n[green]✓ Notes file created: {notes_file}[/green]\n")
        
        # Open in default editor
        editor = config_mgr.get('editor', 'nano')
        subprocess.run([editor, str(notes_file)])
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@notes.command()
@click.option('--machine', help='Machine name (uses current target if not specified)')
def open(machine):
    """Open notes file for a machine"""
    try:
        config_mgr = ConfigManager()
        
        if not machine:
            target_info = config_mgr.get('current_target')
            if not target_info:
                console.print("[red]✗ No machine specified and no current target set[/red]")
                return
            machine = target_info.get('name')
        
        workspace = config_mgr.ensure_workspace()
        notes_dir = workspace / machine.lower() / 'notes'
        notes_file = notes_dir / f'{machine.lower()}_notes.md'
        
        if not notes_file.exists():
            console.print(f"[yellow]⚠ Notes file not found[/yellow]")
            if click.confirm("Do you want to create it?"):
                from htb_cli.commands.notes import create as create_notes
                ctx = click.get_current_context()
                ctx.invoke(create_notes, machine=machine)
            return
        
        editor = config_mgr.get('editor', 'nano')
        subprocess.run([editor, str(notes_file)])
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@notes.command()
def list():
    """List all notes files"""
    try:
        config_mgr = ConfigManager()
        workspace = config_mgr.ensure_workspace()
        
        notes_files = list(workspace.glob('*/notes/*.md'))
        
        if not notes_files:
            console.print("\n[yellow]⚠ No notes files found[/yellow]\n")
            return
        
        console.print("\n[cyan]Notes Files:[/cyan]\n")
        
        for notes_file in sorted(notes_files):
            machine_name = notes_file.parent.parent.name
            modified = datetime.fromtimestamp(notes_file.stat().st_mtime)
            console.print(f"  • [{machine_name}] {notes_file.name} - {modified.strftime('%Y-%m-%d %H:%M')}")
        
        console.print()
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@notes.command()
@click.argument('content', nargs=-1, required=True)
def add(content):
    """Quick add a note to current target"""
    try:
        config_mgr = ConfigManager()
        target_info = config_mgr.get('current_target')
        
        if not target_info:
            console.print("[red]✗ No current target set[/red]")
            return
        
        machine = target_info.get('name')
        workspace = config_mgr.ensure_workspace()
        notes_dir = workspace / machine.lower() / 'notes'
        notes_dir.mkdir(parents=True, exist_ok=True)
        
        notes_file = notes_dir / f'{machine.lower()}_notes.md'
        
        note_text = ' '.join(content)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(notes_file, 'a') as f:
            f.write(f"\n[{timestamp}] {note_text}\n")
        
        console.print(f"\n[green]✓ Note added to {machine}[/green]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()
