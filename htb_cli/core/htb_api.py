"""HackTheBox API client"""

import requests
from typing import Dict, List, Optional, Any
from htb_cli.core.config_manager import ConfigManager


class HTBAPIError(Exception):
    """HTB API Error"""
    pass


class HTBAPIClient:
    """Client for HackTheBox API"""
    
    BASE_URL = "https://labs.hackthebox.com/api/v4"
    
    def __init__(self):
        self.config = ConfigManager()
        self.api_token = self.config.get_api_token()
        if not self.api_token:
            raise HTBAPIError("API token not configured. Run 'htb-cli init' first.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request"""
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise HTBAPIError("Authentication failed. Check your API token.")
            elif e.response.status_code == 403:
                raise HTBAPIError("Access forbidden. VIP subscription may be required.")
            elif e.response.status_code == 404:
                raise HTBAPIError("Resource not found.")
            else:
                raise HTBAPIError(f"API request failed: {e}")
        except requests.exceptions.RequestException as e:
            raise HTBAPIError(f"Network error: {e}")
    
    def get_active_machines(self) -> List[Dict[str, Any]]:
        """Get list of active machines"""
        data = self._request("GET", "machine/list")
        return data.get("info", [])
    
    def get_machine_info(self, machine_id: int) -> Dict[str, Any]:
        """Get detailed information about a machine"""
        return self._request("GET", f"machine/profile/{machine_id}")
    
    def start_machine(self, machine_id: int) -> Dict[str, Any]:
        """Start/spawn a machine"""
        return self._request("POST", f"machine/play/{machine_id}")
    
    def stop_machine(self) -> Dict[str, Any]:
        """Stop currently running machine"""
        return self._request("POST", "machine/stop")
    
    def get_active_machine(self) -> Optional[Dict[str, Any]]:
        """Get currently active/spawned machine"""
        data = self._request("GET", "machine/active")
        return data.get("info")
    
    def submit_flag(self, machine_id: int, flag: str, difficulty: int) -> Dict[str, Any]:
        """Submit a flag"""
        payload = {
            "flag": flag,
            "difficulty": difficulty
        }
        return self._request("POST", f"machine/own/{machine_id}", json=payload)
    
    def get_vpn_servers(self) -> List[Dict[str, Any]]:
        """Get list of VPN servers"""
        data = self._request("GET", "connections/servers")
        return data.get("info", [])
    
    def download_vpn_config(self, server_id: int) -> bytes:
        """Download VPN configuration file"""
        # This endpoint returns raw OVPN file
        url = f"{self.BASE_URL}/access/ovpnfile/{server_id}/0"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            raise HTBAPIError(f"Failed to download VPN config: {e}")
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get current user information"""
        return self._request("GET", "user/info")
