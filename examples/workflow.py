#!/usr/bin/env python3
"""
HTB-CLI Example Usage Script
Demonstrates common workflows and automation
"""

import subprocess
import sys

def run_cmd(cmd):
    """Run a command and print output"""
    print(f"\n{'='*60}")
    print(f"Running: {cmd}")
    print('='*60)
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def example_workflow():
    """Example workflow for attacking a machine"""
    
    print("""
╔════════════════════════════════════════════════════════════╗
║           HTB-CLI Example Workflow                         ║
║                                                            ║
║  This script demonstrates a typical HTB machine workflow  ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # 1. List machines
    print("\n[STEP 1] Listing available machines...")
    if not run_cmd("htb-cli machines list --status active --difficulty easy"):
        return False
    
    # 2. Get machine name from user
    print("\n" + "="*60)
    machine_name = input("Enter machine name to attack: ").strip()
    if not machine_name:
        print("No machine name provided. Exiting.")
        return False
    
    # 3. Start the machine
    print(f"\n[STEP 2] Starting machine '{machine_name}'...")
    if not run_cmd(f"htb-cli machines start {machine_name}"):
        print("Failed to start machine. It might already be running.")
    
    # 4. Get machine info
    print(f"\n[STEP 3] Getting machine information...")
    run_cmd(f"htb-cli machines info {machine_name}")
    
    # 5. Get IP address
    print("\n" + "="*60)
    ip_address = input("Enter the machine IP address: ").strip()
    if not ip_address:
        print("No IP provided. Exiting.")
        return False
    
    # 6. Set target
    print(f"\n[STEP 4] Setting target...")
    if not run_cmd(f"htb-cli target set {machine_name} {ip_address}"):
        return False
    
    # 7. Add to hosts
    print(f"\n[STEP 5] Adding to /etc/hosts...")
    run_cmd("htb-cli target hosts --add")
    
    # 8. Show target info
    print(f"\n[STEP 6] Target information...")
    run_cmd("htb-cli target show")
    
    # 9. Quick scan
    print(f"\n[STEP 7] Running quick port scan...")
    if not run_cmd("htb-cli scan quick"):
        return False
    
    # 10. Ask about full scan
    print("\n" + "="*60)
    if input("Run full scan? (y/n): ").lower() == 'y':
        print(f"\n[STEP 8] Running full scan...")
        run_cmd("htb-cli scan full")
    
    # 11. Ask about web scan
    print("\n" + "="*60)
    if input("Run web enumeration? (y/n): ").lower() == 'y':
        print(f"\n[STEP 9] Running web enumeration...")
        run_cmd("htb-cli scan web")
    
    # 12. Create notes
    print(f"\n[STEP 10] Creating notes file...")
    run_cmd("htb-cli notes create")
    
    # 13. Show workspace
    print(f"\n[STEP 11] Opening workspace...")
    run_cmd("htb-cli target workspace")
    
    print("""
╔════════════════════════════════════════════════════════════╗
║                 Workflow Complete!                         ║
║                                                            ║
║  Your environment is now set up for attacking the machine ║
║                                                            ║
║  Next steps:                                               ║
║  1. Review scan results                                    ║
║  2. Research vulnerabilities                               ║
║  3. Exploit and capture flags!                             ║
║                                                            ║
║  Useful commands:                                          ║
║  - htb-cli exploit shell --type bash                       ║
║  - htb-cli exploit listen --port 4444                      ║
║  - htb-cli notes add "your findings"                       ║
║  - htb-cli scan list                                       ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    return True

def main():
    """Main entry point"""
    try:
        if not example_workflow():
            print("\n[ERROR] Workflow failed. Please check the output above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n[INFO] Workflow interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
