#!/bin/bash

# HTB-CLI Quick Reference Card
# Save this and keep it handy!

cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║                        HTB-CLI QUICK REFERENCE                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─ INITIAL SETUP ──────────────────────────────────────────────────────────────┐
│ htb-cli init                              # Initial configuration            │
│ htb-cli config show                       # Show current config              │
│ htb-cli config set-token <token>          # Update API token                │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ VPN MANAGEMENT ─────────────────────────────────────────────────────────────┐
│ htb-cli vpn servers                       # List available servers           │
│ htb-cli vpn download --server us-vip-1    # Download VPN config             │
│ htb-cli vpn connect                       # Connect to VPN                   │
│ htb-cli vpn status                        # Check VPN status                 │
│ htb-cli vpn disconnect                    # Disconnect VPN                   │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ MACHINE MANAGEMENT ─────────────────────────────────────────────────────────┐
│ htb-cli machines list                     # List all active machines         │
│ htb-cli machines list --difficulty easy   # Filter by difficulty             │
│ htb-cli machines info <name>              # Get machine details              │
│ htb-cli machines start <name>             # Start a machine                  │
│ htb-cli machines active                   # Show active machine              │
│ htb-cli machines stop                     # Stop current machine             │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ TARGET SETUP ───────────────────────────────────────────────────────────────┐
│ htb-cli target set <name> <ip>            # Set current target               │
│ htb-cli target show                       # Show current target              │
│ htb-cli target export --shell zsh         # Export env variables             │
│ htb-cli target hosts --add                # Add to /etc/hosts                │
│ htb-cli target workspace                  # Open workspace folder            │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ SCANNING ───────────────────────────────────────────────────────────────────┐
│ htb-cli scan quick                        # Quick port scan (top 1000)       │
│ htb-cli scan full                         # Full port scan                   │
│ htb-cli scan full --ports 22,80,443       # Scan specific ports              │
│ htb-cli scan web                          # Web directory enumeration        │
│ htb-cli scan udp                          # UDP scan                         │
│ htb-cli scan list                         # List all scan results            │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ EXPLOITATION ───────────────────────────────────────────────────────────────┐
│ htb-cli exploit shell --type bash         # Generate reverse shell           │
│ htb-cli exploit listen --port 4444        # Start netcat listener            │
│ htb-cli exploit serve --port 80           # Start HTTP server                │
│ htb-cli exploit upgrade                   # Shell upgrade commands           │
│ htb-cli exploit privesc                   # Privesc checklist                │
│ htb-cli exploit download --method wget    # File download commands           │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ NOTES & DOCUMENTATION ──────────────────────────────────────────────────────┐
│ htb-cli notes create                      # Create notes file                │
│ htb-cli notes open                        # Open notes in editor             │
│ htb-cli notes add "finding text"          # Quick add note                   │
│ htb-cli notes list                        # List all notes                   │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ TYPICAL WORKFLOW ───────────────────────────────────────────────────────────┐
│ 1. htb-cli machines list                  # Find a machine                   │
│ 2. htb-cli machines start <name>          # Start it                         │
│ 3. htb-cli target set <name> <ip>         # Set as target                    │
│ 4. htb-cli target hosts --add             # Add to /etc/hosts                │
│ 5. eval $(htb-cli target export)          # Export env vars                  │
│ 6. htb-cli scan quick                     # Initial scan                     │
│ 7. htb-cli scan full                      # Detailed scan                    │
│ 8. htb-cli notes create                   # Start documentation              │
│ 9. htb-cli exploit shell --type bash      # Get reverse shell payload        │
│ 10. htb-cli exploit listen                # Start listener                   │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ USEFUL ALIASES ─────────────────────────────────────────────────────────────┐
│ alias htb='htb-cli'                                                           │
│ alias htb-ls='htb-cli machines list --status active'                         │
│ alias htb-info='htb-cli target show'                                         │
│ alias htb-scan='htb-cli scan quick && htb-cli scan full'                     │
│ alias htb-vpn='htb-cli vpn status'                                           │
│ alias htb-shell='htb-cli exploit shell'                                      │
│ alias htb-nc='htb-cli exploit listen'                                        │
└──────────────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════════════╗
║  For detailed help on any command: htb-cli <command> --help                 ║
║  Documentation: /home/kali/Desktop/HTB-CLI/USAGE.md                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

EOF
