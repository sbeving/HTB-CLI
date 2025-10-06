"""Configuration management for HTB-CLI"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages HTB-CLI configuration"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".htb-cli"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._config: Optional[Dict[str, Any]] = None
    
    def config_exists(self) -> bool:
        """Check if configuration file exists"""
        return self.config_file.exists()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self._config is None:
            if self.config_exists():
                with open(self.config_file, 'r') as f:
                    self._config = json.load(f)
            else:
                self._config = {}
        return self._config
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file"""
        self._config = config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        config = self.load_config()
        keys = key.split('.')
        value = config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        config = self.load_config()
        keys = key.split('.')
        current = config
        
        for i, k in enumerate(keys[:-1]):
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
        self.save_config(config)
    
    def get_api_token(self) -> Optional[str]:
        """Get HTB API token"""
        return self.get('api_token')
    
    def get_workspace(self) -> str:
        """Get workspace directory"""
        workspace = self.get('workspace', '~/htb')
        return os.path.expanduser(workspace)
    
    def ensure_workspace(self) -> Path:
        """Ensure workspace directory exists"""
        workspace = Path(self.get_workspace())
        workspace.mkdir(parents=True, exist_ok=True)
        return workspace
