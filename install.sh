#!/usr/bin/env bash

# HTB-CLI Installation Script

set -e

echo "=================================="
echo "HTB-CLI Installation"
echo "=================================="
echo ""

# Check Python version
echo "[*] Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "    Python version: $python_version"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "[!] pip3 not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Check for required tools
echo ""
echo "[*] Checking required tools..."
required_tools=("nmap" "openvpn" "gobuster" "curl")
missing_tools=()

for tool in "${required_tools[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "    ✓ $tool found"
    else
        echo "    ✗ $tool not found"
        missing_tools+=($tool)
    fi
done

if [ ${#missing_tools[@]} -gt 0 ]; then
    echo ""
    echo "[!] Missing tools detected: ${missing_tools[*]}"
    read -p "Do you want to install them? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt-get update
        sudo apt-get install -y "${missing_tools[@]}"
    fi
fi

# Install Python package
echo ""
echo "[*] Installing HTB-CLI..."
pip3 install -e .

# Make main script executable
chmod +x htb_cli/main.py

# Add to PATH (optional)
echo ""
read -p "Do you want to add HTB-CLI to your PATH? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    install_dir=$(pwd)
    
    # Detect shell
    if [ -n "$ZSH_VERSION" ]; then
        shell_rc="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        shell_rc="$HOME/.bashrc"
    else
        shell_rc="$HOME/.profile"
    fi
    
    # Add to PATH if not already there
    if ! grep -q "HTB-CLI" "$shell_rc"; then
        echo "" >> "$shell_rc"
        echo "# HTB-CLI" >> "$shell_rc"
        echo "export PATH=\"\$PATH:$install_dir\"" >> "$shell_rc"
        echo "    ✓ Added to $shell_rc"
    else
        echo "    Already in PATH"
    fi
fi

echo ""
echo "=================================="
echo "Installation Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Get your HTB API token from: https://app.hackthebox.com/profile/settings"
echo "2. Run: htb-cli init"
echo "3. Start hacking: htb-cli machines list"
echo ""
echo "For help, run: htb-cli --help"
echo ""
