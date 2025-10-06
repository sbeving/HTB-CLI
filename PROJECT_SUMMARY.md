# HTB-CLI - Complete Project Summary

## 🎯 Overview

HTB-CLI is a comprehensive command-line utility designed to automate and streamline your HackTheBox workflow. It provides a unified interface for machine management, VPN connectivity, scanning, exploitation, and documentation.

## ✨ Features Implemented

### 1. **Machine Management** (`htb-cli machines`)
- ✅ List machines with advanced filtering (OS, difficulty, status)
- ✅ Search machines by name
- ✅ Get detailed machine information
- ✅ Start/stop machines via API
- ✅ Show currently active machine
- ✅ Submit flags (user/root)

### 2. **VPN Management** (`htb-cli vpn`)
- ✅ List available VPN servers
- ✅ Download VPN configurations
- ✅ Connect/disconnect from VPN
- ✅ Check VPN connection status
- ✅ Auto-detect VPN IP address

### 3. **Target Management** (`htb-cli target`)
- ✅ Set current target machine
- ✅ Auto-create workspace directories
- ✅ Export environment variables (TARGET_IP, TARGET_NAME, TARGET_DOMAIN)
- ✅ Manage /etc/hosts entries
- ✅ Open workspace in file manager
- ✅ Show current target information

### 4. **Scanning** (`htb-cli scan`)
- ✅ Quick port scan (top 1000 ports)
- ✅ Full comprehensive scan with service detection
- ✅ Web directory enumeration (gobuster)
- ✅ UDP port scanning
- ✅ Auto-save results with timestamps
- ✅ List all scan results

### 5. **Exploitation Helpers** (`htb-cli exploit`)
- ✅ Reverse shell payload generator (bash, python, nc, php, perl, powershell)
- ✅ URL encoding and Base64 encoding of payloads
- ✅ Netcat listener starter
- ✅ HTTP server for file transfers
- ✅ SSH tunnel helper
- ✅ Shell upgrade techniques
- ✅ File download method generator
- ✅ Privilege escalation checklist

### 6. **Notes & Documentation** (`htb-cli notes`)
- ✅ Create structured notes with templates
- ✅ Quick add notes to current target
- ✅ Open notes in preferred editor
- ✅ List all notes files
- ✅ Auto-generate writeup templates

### 7. **Configuration** (`htb-cli config`)
- ✅ Initialize configuration wizard
- ✅ Show/edit configuration
- ✅ Set/get individual config values
- ✅ Update API token
- ✅ Show config file location

## 📁 Project Structure

```
HTB-CLI/
├── htb_cli/
│   ├── __init__.py
│   ├── main.py                    # Main CLI entry point
│   ├── utils.py                   # Utility functions
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config_manager.py      # Configuration management
│   │   └── htb_api.py             # HTB API client
│   └── commands/
│       ├── __init__.py
│       ├── machines.py            # Machine commands
│       ├── vpn.py                 # VPN commands
│       ├── target.py              # Target commands
│       ├── scan.py                # Scanning commands
│       ├── exploit.py             # Exploit helpers
│       ├── notes.py               # Notes commands
│       └── config.py              # Config commands
├── tests/
│   ├── __init__.py
│   └── test_htb_cli.py           # Unit tests
├── examples/
│   └── workflow.py               # Example workflow script
├── docs/
├── install.sh                    # Installation script
├── quickstart.sh                 # Shell helpers
├── cheatsheet.sh                 # Quick reference
├── setup.py                      # Package setup
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Development dependencies
├── config.example.json           # Example configuration
├── README.md                     # Main documentation
├── USAGE.md                      # Detailed usage guide
├── CONTRIBUTING.md               # Contribution guidelines
├── ROADMAP.md                    # Future plans
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore rules
```

## 🚀 Installation

```bash
cd /home/kali/Desktop/HTB-CLI
chmod +x install.sh
./install.sh
```

## ⚙️ Quick Setup

```bash
# 1. Initialize configuration
htb-cli init

# 2. Connect to VPN
htb-cli vpn download --server us-vip-1
htb-cli vpn connect

# 3. Start hacking!
htb-cli machines list
```

## 📖 Usage Examples

### Starting a Machine
```bash
htb-cli machines list --difficulty easy
htb-cli machines start Bashed
htb-cli target set Bashed 10.10.10.68
htb-cli target hosts --add
```

### Scanning
```bash
htb-cli scan quick
htb-cli scan full --ports 22,80,443
htb-cli scan web http://10.10.10.68
```

### Exploitation
```bash
# Generate reverse shell
htb-cli exploit shell --type bash --port 4444

# Start listener
htb-cli exploit listen --port 4444

# Serve files
htb-cli exploit serve --port 80
```

### Documentation
```bash
htb-cli notes create
htb-cli notes add "Found SQL injection in login form"
htb-cli notes open
```

## 🛠️ Technologies Used

- **Python 3.8+** - Core language
- **Click** - CLI framework
- **Rich** - Terminal formatting
- **Requests** - HTTP client for API
- **Nmap** - Port scanning
- **OpenVPN** - VPN connectivity
- **Gobuster** - Web enumeration

## 📊 Workspace Organization

Each machine gets an organized workspace:

```
~/htb/
└── machine-name/
    ├── scans/          # All scan results (nmap, gobuster)
    ├── exploits/       # Exploit code and payloads
    ├── loot/           # Credentials, files, flags
    └── notes/          # Documentation and writeups
```

## 🎨 Key Design Features

1. **Modular Architecture** - Each command group in separate file
2. **Rich CLI Interface** - Colored output, tables, and formatting
3. **Auto-Workspace Creation** - Organized directory structure
4. **Environment Integration** - Export variables for other tools
5. **Error Handling** - Comprehensive error messages
6. **Configuration Management** - Centralized settings
7. **API Integration** - Direct HTB platform interaction
8. **Extensible** - Easy to add new commands

## 🔧 Configuration

Configuration stored in `~/.htb-cli/config.json`:

```json
{
  "api_token": "your_htb_token",
  "workspace": "~/htb",
  "vpn": {
    "default_server": "us-vip-1",
    "auto_connect": false
  },
  "scan": {
    "default_threads": "1000",
    "save_results": true
  },
  "current_target": {
    "name": "Machine",
    "ip": "10.10.10.10",
    "domain": "machine.htb"
  }
}
```

## 📚 Documentation

- **README.md** - Project overview and quick start
- **USAGE.md** - Comprehensive usage guide (35+ examples)
- **CONTRIBUTING.md** - Contribution guidelines
- **ROADMAP.md** - Future development plans
- **cheatsheet.sh** - Quick reference card

## 🧪 Testing

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=htb_cli
```

## 🔐 Security Features

- API token stored securely in config
- Sensitive data masked in config display
- VPN status checking
- Sudo prompts for privileged operations

## 🌟 Unique Features

1. **One-Command Target Setup** - Automatically creates workspace, exports vars, updates hosts
2. **Smart Defaults** - Uses current target if IP not specified
3. **Shell Helper Functions** - Source quickstart.sh for additional aliases
4. **Auto-Timestamped Scans** - Never overwrite previous results
5. **Multi-Format Output** - URL encoded, Base64, etc. for payloads
6. **Integrated Workflow** - Seamless machine-to-exploitation flow

## 🎯 Use Cases

### Penetration Testing
- Rapid reconnaissance and enumeration
- Organized scan result management
- Quick exploit payload generation

### CTF Competitions
- Fast machine switching
- Automated first blood attempts
- Progress tracking and notes

### Learning & Practice
- Structured approach to machines
- Documentation templates
- Command history in notes

### Team Collaboration
- Shared workspace structure
- Standardized workflows
- Easy knowledge transfer

## 🚦 Getting Started Workflow

```bash
# 1. Install and setup
./install.sh
htb-cli init

# 2. Connect to VPN
htb-cli vpn download
htb-cli vpn connect

# 3. Choose and start machine
htb-cli machines list --difficulty easy
htb-cli machines start <machine>

# 4. Set up target
htb-cli target set <machine> <ip>
eval $(htb-cli target export --shell zsh)

# 5. Enumerate
htb-cli scan quick
htb-cli scan full

# 6. Document findings
htb-cli notes create

# 7. Exploit
htb-cli exploit shell --type bash
htb-cli exploit listen

# 8. Submit flags
htb-cli machines submit <machine> <flag> --user
htb-cli machines submit <machine> <flag> --root
```

## 📈 Performance

- Quick scan: ~30-60 seconds
- Full scan: 5-15 minutes (depending on ports)
- API calls: < 1 second
- VPN connection: ~5-10 seconds

## 🤝 Contributing

We welcome contributions! See CONTRIBUTING.md for:
- Code style guidelines
- Development setup
- Pull request process
- Testing requirements

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- HackTheBox for the platform and API
- Click framework for CLI structure
- Rich library for beautiful terminal output
- The infosec community for inspiration

## 📞 Support

- GitHub Issues: Report bugs and request features
- Documentation: Check USAGE.md for detailed help
- Examples: See examples/ directory for workflows

## 🎓 Learning Resources

The project demonstrates:
- Python CLI development with Click
- API client implementation
- Configuration management
- Subprocess handling
- Error handling and validation
- Terminal UI design
- Test-driven development
- Documentation best practices

## 🔮 Future Enhancements

See ROADMAP.md for planned features:
- Automated exploit suggestion
- CVE lookup integration
- Web vulnerability scanning
- Multi-machine management
- Team collaboration features
- Machine learning integration

---

**HTB-CLI** - Automate your HackTheBox workflow and hack faster! 🚀

Made with ❤️ for the cybersecurity community.
