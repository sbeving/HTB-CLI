# HTB-CLI Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Initial Setup](#initial-setup)
3. [Common Workflows](#common-workflows)
4. [Command Reference](#command-reference)
5. [Tips & Tricks](#tips--tricks)

---

## Installation

### Quick Install
```bash
cd /home/kali/Desktop/HTB-CLI
chmod +x install.sh
./install.sh
```

### Manual Install
```bash
# Install dependencies
pip3 install -r requirements.txt

# Install package
pip3 install -e .

# Verify installation
htb-cli --version
```

### Required Tools
- `nmap` - Port scanning
- `openvpn` - VPN connectivity
- `gobuster` - Web enumeration
- `curl` - API requests

Install on Kali Linux:
```bash
sudo apt update
sudo apt install nmap openvpn gobuster curl -y
```

---

## Initial Setup

### 1. Get Your HTB API Token
1. Go to https://app.hackthebox.com/profile/settings
2. Navigate to "App Tokens" section
3. Generate a new token or copy existing one

### 2. Initialize HTB-CLI
```bash
htb-cli init
```

This will prompt you for:
- HTB API token
- Workspace directory (default: `~/htb`)
- Default VPN server (e.g., `us-vip-1`)

### 3. Verify Configuration
```bash
htb-cli config show
```

---

## Common Workflows

### Workflow 1: Starting a New Machine

```bash
# 1. List available machines
htb-cli machines list --status active --difficulty easy

# 2. Start a machine
htb-cli machines start <machine-name>

# 3. Set as current target (auto-creates workspace)
htb-cli target set <machine-name> <ip-address>

# 4. Add to /etc/hosts
htb-cli target hosts --add

# 5. Export environment variables
eval $(htb-cli target export --shell zsh)

# 6. Quick port scan
htb-cli scan quick

# 7. Full scan on discovered ports
htb-cli scan full --ports 22,80,443

# 8. Web enumeration (if web server found)
htb-cli scan web
```

### Workflow 2: VPN Management

```bash
# List available VPN servers
htb-cli vpn servers

# Download VPN config
htb-cli vpn download --server us-vip-1

# Connect to VPN
htb-cli vpn connect

# Check connection status
htb-cli vpn status

# Disconnect
htb-cli vpn disconnect
```

### Workflow 3: Note Taking

```bash
# Create notes for current target
htb-cli notes create

# Quick add a note
htb-cli notes add "Found SQL injection in login form"

# Open notes for editing
htb-cli notes open

# List all notes
htb-cli notes list
```

### Workflow 4: Flag Submission

```bash
# Submit user flag
htb-cli machines submit <machine-name> <flag> --user

# Submit root flag
htb-cli machines submit <machine-name> <flag> --root
```

---

## Command Reference

### Machines
```bash
# List machines with filters
htb-cli machines list [--status active|retired|all] [--os linux|windows|all] [--difficulty easy|medium|hard|insane|all]

# Get machine info
htb-cli machines info <machine-name>

# Start a machine
htb-cli machines start <machine-name>

# Stop current machine
htb-cli machines stop

# Show active machine
htb-cli machines active

# Submit flag
htb-cli machines submit <machine-name> <flag> [--user|--root]
```

### VPN
```bash
# List VPN servers
htb-cli vpn servers

# Download VPN config
htb-cli vpn download [--server <server-name>] [--output <path>]

# Connect to VPN
htb-cli vpn connect [--config <path>]

# Disconnect from VPN
htb-cli vpn disconnect

# Check VPN status
htb-cli vpn status
```

### Target
```bash
# Set current target
htb-cli target set <machine-name> <ip> [--domain <domain>]

# Show current target
htb-cli target show

# Export environment variables
htb-cli target export [--shell bash|zsh|fish]

# Manage /etc/hosts
htb-cli target hosts --add
htb-cli target hosts --remove

# Open workspace directory
htb-cli target workspace
```

### Scanning
```bash
# Quick scan (top 1000 ports)
htb-cli scan quick [target] [--ports 1-1000] [--threads 1000]

# Full scan
htb-cli scan full [target] [--ports <ports>] [--scripts default,vuln]

# Web enumeration
htb-cli scan web [target] [--wordlist <path>] [--extensions php,html,txt]

# UDP scan
htb-cli scan udp [target]

# List scan results
htb-cli scan list
```

### Notes
```bash
# Create notes for machine
htb-cli notes create [--machine <name>]

# Open notes
htb-cli notes open [--machine <name>]

# Quick add note
htb-cli notes add <text>

# List all notes
htb-cli notes list
```

### Configuration
```bash
# Show all config
htb-cli config show

# Get config value
htb-cli config get <key>

# Set config value
htb-cli config set <key> <value>

# Set API token
htb-cli config set-token <token>

# Show config file path
htb-cli config path
```

---

## Tips & Tricks

### 1. Use Shell Helpers
Source the quickstart script for additional helper functions:
```bash
source /home/kali/Desktop/HTB-CLI/quickstart.sh
```

This adds useful functions like:
- `htb-export` - Quick target setup
- `htb-scan` - Fast scanning
- `htb-listen` - Start netcat listener
- `htb-shell` - Generate reverse shells

### 2. Environment Variables
After setting a target, export variables for easy access:
```bash
eval $(htb-cli target export --shell zsh)
echo $TARGET_IP
echo $TARGET_NAME
echo $TARGET_DOMAIN
```

Use in your own scripts:
```bash
nmap -sV -sC $TARGET_IP
gobuster dir -u http://$TARGET_DOMAIN -w /usr/share/wordlists/dirb/common.txt
```

### 3. Workspace Organization
HTB-CLI automatically creates this structure:
```
~/htb/
  └── machine-name/
      ├── scans/      # All scan results
      ├── exploits/   # Exploit code
      ├── loot/       # Credentials, files found
      └── notes/      # Documentation
```

### 4. Quick Scanning Pattern
```bash
# 1. Quick scan to find open ports
htb-cli scan quick
# Note the open ports from output

# 2. Detailed scan on those ports
htb-cli scan full --ports 22,80,443,8080

# 3. If web server found
htb-cli scan web http://$TARGET_IP
```

### 5. Automating Repetitive Tasks
Create aliases in your `.zshrc`:
```bash
alias htb='htb-cli'
alias htb-ls='htb-cli machines list --status active'
alias htb-start='htb-cli machines start'
alias htb-scan='htb-cli scan quick && htb-cli scan full'
```

### 6. Integration with Other Tools

**With tmux:**
```bash
# Terminal 1: VPN and scans
tmux new-session -s htb
htb-cli vpn connect
htb-cli scan quick

# Terminal 2: Notes
tmux split-window -h
htb-cli notes open

# Terminal 3: Exploitation
tmux split-window -v
nc -lvnp 4444
```

**With metasploit:**
```bash
# Export target
eval $(htb-cli target export --shell zsh)

# Use in msfconsole
msfconsole -x "setg RHOSTS $TARGET_IP; setg LHOST tun0"
```

### 7. Backing Up Your Work
```bash
# Backup all machine workspaces
tar -czf htb-backup-$(date +%Y%m%d).tar.gz ~/htb/

# Backup specific machine
tar -czf machine-backup.tar.gz ~/htb/machine-name/
```

### 8. Troubleshooting

**API Token Issues:**
```bash
# Verify token
htb-cli config get api_token

# Update token
htb-cli config set-token <new-token>
```

**VPN Issues:**
```bash
# Check status
htb-cli vpn status

# Reconnect
htb-cli vpn disconnect
htb-cli vpn connect

# Manual check
ip addr show tun0
```

**Scan Results Not Saving:**
```bash
# Check workspace
htb-cli config get workspace

# Verify target is set
htb-cli target show

# Check permissions
ls -la ~/htb/
```

---

## Advanced Usage

### Custom Scan Profiles
Edit scan commands for your preferences:
```bash
# Add to config
htb-cli config set scan.quick_args "-sS -T4 --min-rate=2000"
htb-cli config set scan.full_args "-sS -sV -sC -A"
```

### Multiple VPN Configs
```bash
# Download multiple regions
htb-cli vpn download --server us-vip-1 --output ~/.htb-cli/vpn/us.ovpn
htb-cli vpn download --server eu-vip-1 --output ~/.htb-cli/vpn/eu.ovpn

# Switch between them
htb-cli vpn connect --config ~/.htb-cli/vpn/us.ovpn
htb-cli vpn connect --config ~/.htb-cli/vpn/eu.ovpn
```

### Tracking Progress
```bash
# Add progress notes
htb-cli notes add "Initial foothold achieved via SSH"
htb-cli notes add "Found user.txt in /home/user/user.txt"
htb-cli notes add "Privilege escalation via sudo misconfiguration"
```

---

## Getting Help

```bash
# General help
htb-cli --help

# Command-specific help
htb-cli machines --help
htb-cli scan --help
htb-cli vpn --help
```

## Support & Contributing

Found a bug or have a feature request? Please open an issue on GitHub!

Happy Hacking! 🚀
