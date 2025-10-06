"""Scanning commands"""

import click
import subprocess
import os
from datetime import datetime
from pathlib import Path
from rich.console import Console
from htb_cli.core.config_manager import ConfigManager

console = Console()


@click.group()
def scan():
    """Run port scans and enumeration"""
    pass


@scan.command()
@click.argument('target', required=False)
@click.option('--ports', default='1-1000', help='Port range to scan')
@click.option('--threads', default='1000', help='Number of threads')
def quick(target, ports, threads):
    """Quick port scan (top 1000 ports)"""
    try:
        config_mgr = ConfigManager()
        
        # Get target from config if not provided
        if not target:
            target_info = config_mgr.get('current_target')
            if not target_info:
                console.print("[red]✗ No target specified and no current target set[/red]")
                return
            target = target_info.get('ip')
            machine_name = target_info.get('name')
        else:
            machine_name = target.replace('.', '_')
        
        console.print(f"\n[cyan]Running quick scan on {target}...[/cyan]")
        console.print(f"[dim]Scanning ports {ports} with {threads} threads[/dim]\n")
        
        # Prepare output directory
        workspace = config_mgr.ensure_workspace()
        scan_dir = workspace / machine_name.lower() / 'scans'
        scan_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = scan_dir / f'quick_scan_{timestamp}'
        
        # Run nmap quick scan
        cmd = (
            f"nmap -p{ports} -T4 --min-rate={threads} "
            f"-oN {output_file}.txt -oX {output_file}.xml "
            f"{target}"
        )
        
        console.print("[yellow]Scanning...[/yellow]")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        console.print(result.stdout)
        
        if result.returncode == 0:
            console.print(f"\n[green]✓ Scan completed![/green]")
            console.print(f"[dim]Results saved to: {output_file}.txt[/dim]\n")
        else:
            console.print(f"\n[red]✗ Scan failed: {result.stderr}[/red]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@scan.command()
@click.argument('target', required=False)
@click.option('--ports', help='Specific ports to scan (comma-separated or range)')
@click.option('--scripts', default='default,vuln', help='NSE scripts to run')
def full(target, ports, scripts):
    """Full comprehensive scan with service detection"""
    try:
        config_mgr = ConfigManager()
        
        # Get target from config if not provided
        if not target:
            target_info = config_mgr.get('current_target')
            if not target_info:
                console.print("[red]✗ No target specified and no current target set[/red]")
                return
            target = target_info.get('ip')
            machine_name = target_info.get('name')
        else:
            machine_name = target.replace('.', '_')
        
        console.print(f"\n[cyan]Running full scan on {target}...[/cyan]")
        console.print("[dim]This may take several minutes...[/dim]\n")
        
        # Prepare output directory
        workspace = config_mgr.ensure_workspace()
        scan_dir = workspace / machine_name.lower() / 'scans'
        scan_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = scan_dir / f'full_scan_{timestamp}'
        
        # Build nmap command
        port_arg = f"-p{ports}" if ports else "-p-"
        
        cmd = (
            f"nmap {port_arg} -sC -sV -A "
            f"--script={scripts} "
            f"-oN {output_file}.txt -oX {output_file}.xml -oG {output_file}.gnmap "
            f"{target}"
        )
        
        console.print("[yellow]Scanning...[/yellow]")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        console.print(result.stdout)
        
        if result.returncode == 0:
            console.print(f"\n[green]✓ Scan completed![/green]")
            console.print(f"[dim]Results saved to: {output_file}.txt[/dim]\n")
        else:
            console.print(f"\n[red]✗ Scan failed: {result.stderr}[/red]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@scan.command()
@click.argument('target', required=False)
@click.option('--wordlist', default='/usr/share/wordlists/dirb/common.txt',
              help='Wordlist for directory enumeration')
@click.option('--extensions', default='php,html,txt,js',
              help='File extensions to search for')
def web(target, wordlist, extensions):
    """Web directory enumeration with gobuster"""
    try:
        config_mgr = ConfigManager()
        
        # Get target from config if not provided
        if not target:
            target_info = config_mgr.get('current_target')
            if not target_info:
                console.print("[red]✗ No target specified and no current target set[/red]")
                return
            target = target_info.get('ip')
            machine_name = target_info.get('name')
        else:
            machine_name = target.replace('.', '_').replace('http://', '').replace('https://', '')
        
        # Check if target is a URL or IP
        if not target.startswith('http'):
            target = f"http://{target}"
        
        console.print(f"\n[cyan]Running web enumeration on {target}...[/cyan]")
        console.print(f"[dim]Wordlist: {wordlist}[/dim]\n")
        
        # Prepare output directory
        workspace = config_mgr.ensure_workspace()
        scan_dir = workspace / machine_name.lower() / 'scans'
        scan_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = scan_dir / f'web_scan_{timestamp}.txt'
        
        # Run gobuster
        cmd = (
            f"gobuster dir -u {target} -w {wordlist} "
            f"-x {extensions} -o {output_file} -q"
        )
        
        console.print("[yellow]Enumerating directories...[/yellow]\n")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        console.print(result.stdout)
        
        if result.returncode == 0 or result.returncode == 1:  # gobuster returns 1 on completion
            console.print(f"\n[green]✓ Enumeration completed![/green]")
            console.print(f"[dim]Results saved to: {output_file}[/dim]\n")
        else:
            console.print(f"\n[red]✗ Enumeration failed: {result.stderr}[/red]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@scan.command()
@click.argument('target', required=False)
def udp(target):
    """UDP port scan (top 100 ports)"""
    try:
        config_mgr = ConfigManager()
        
        # Get target from config if not provided
        if not target:
            target_info = config_mgr.get('current_target')
            if not target_info:
                console.print("[red]✗ No target specified and no current target set[/red]")
                return
            target = target_info.get('ip')
            machine_name = target_info.get('name')
        else:
            machine_name = target.replace('.', '_')
        
        console.print(f"\n[cyan]Running UDP scan on {target}...[/cyan]")
        console.print("[dim]Scanning top 100 UDP ports (this may take a while)...[/dim]\n")
        
        # Prepare output directory
        workspace = config_mgr.ensure_workspace()
        scan_dir = workspace / machine_name.lower() / 'scans'
        scan_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = scan_dir / f'udp_scan_{timestamp}'
        
        # Run nmap UDP scan (requires sudo)
        cmd = (
            f"sudo nmap -sU --top-ports 100 "
            f"-oN {output_file}.txt -oX {output_file}.xml "
            f"{target}"
        )
        
        console.print("[yellow]Scanning (requires sudo)...[/yellow]")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        console.print(result.stdout)
        
        if result.returncode == 0:
            console.print(f"\n[green]✓ Scan completed![/green]")
            console.print(f"[dim]Results saved to: {output_file}.txt[/dim]\n")
        else:
            console.print(f"\n[red]✗ Scan failed: {result.stderr}[/red]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@scan.command()
def list():
    """List all scan results for current target"""
    try:
        config_mgr = ConfigManager()
        target_info = config_mgr.get('current_target')
        
        if not target_info:
            console.print("[red]✗ No target set[/red]")
            return
        
        machine_name = target_info.get('name')
        workspace = config_mgr.ensure_workspace()
        scan_dir = workspace / machine_name.lower() / 'scans'
        
        if not scan_dir.exists():
            console.print(f"[yellow]⚠ No scans found for {machine_name}[/yellow]\n")
            return
        
        scan_files = sorted(scan_dir.glob('*.txt'), key=lambda p: p.stat().st_mtime, reverse=True)
        
        if not scan_files:
            console.print(f"[yellow]⚠ No scan results found[/yellow]\n")
            return
        
        console.print(f"\n[cyan]Scan results for {machine_name}:[/cyan]\n")
        
        for scan_file in scan_files:
            size = scan_file.stat().st_size
            modified = datetime.fromtimestamp(scan_file.stat().st_mtime)
            console.print(f"  • {scan_file.name} ({size} bytes) - {modified.strftime('%Y-%m-%d %H:%M')}")
        
        console.print()
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()
