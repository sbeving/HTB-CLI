# HTB-CLI - HackTheBox Command Line Utility

A comprehensive CLI tool to automate your HackTheBox workflow.

## Features

- 🖥️  **Machine Management**
  - List active/retired machines with filters (OS, difficulty, rating)
  - Get machine details and information
  - Start/stop machines
  
- 🔌 **VPN Management**
  - Download VPN configurations
  - Switch between VPN servers (regions)
  - Auto-connect to VPN
  - Check VPN connection status

- 🎯 **Target Management**
  - Export target IP to environment variables
  - Auto-generate /etc/hosts entries
  - Quick target switching between machines

- 🚀 **Scanning & Enumeration**
  - Fast initial port scans (top ports)
  - Full comprehensive scans
  - Service enumeration templates
  - Auto-save scan results organized by machine

- 💉 **Exploit Workflow**
  - Track first blood attempts
  - Store exploit notes and payloads
  - Quick reverse shell generators
  - Privilege escalation checklists

- 📝 **Notes & Documentation**
  - Auto-generate machine writeup templates
  - Track progress and findings
  - Export notes in markdown format

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/HTB-CLI.git
cd HTB-CLI

# Install dependencies
pip install -r requirements.txt

# Configure HTB API token
htb-cli config set-token YOUR_HTB_APP_TOKEN

# Optional: Add to PATH
echo 'export PATH="$PATH:/home/kali/Desktop/HTB-CLI"' >> ~/.zshrc
source ~/.zshrc
```

## Quick Start

```bash
# Initialize configuration
htb-cli init

# List active machines
htb-cli machines list --status active

# Start a machine
htb-cli machines start <machine-name>

# Set target
htb-cli target set <machine-name> <ip>

# Download and connect to VPN
htb-cli vpn download --server us-vip-1
htb-cli vpn connect

# Quick scan
htb-cli scan quick <ip>

# Full scan
htb-cli scan full <ip> --output scans/<machine-name>
```

## Configuration

The tool stores configuration in `~/.htb-cli/config.json`:
- HTB API token
- Default VPN server
- Scan preferences
- Target workspace directory

## Requirements

- Python 3.8+
- OpenVPN
- nmap
- curl/wget
- Valid HackTheBox account and API token

## License

MIT License
