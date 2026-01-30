"""
tools/wifi.py — Toggle Wi‑Fi using netsh (Windows).
Note: requires Administrator privileges to change interface state.
"""
import subprocess
import ctypes
import re

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def _find_wifi_interface():
    """Return the interface name for Wi-Fi using `netsh interface show interface` parsing."""
    try:
        out = subprocess.check_output(["netsh", "interface", "show", "interface"], text=True, stderr=subprocess.DEVNULL)
        # parse lines like: Enabled    Connected     Dedicated    Wi-Fi
        for line in out.splitlines():
            if "Wi-Fi" in line or "Wireless" in line or "Wireless LAN" in line:
                # last token is name
                parts = line.split()
                if parts:
                    return parts[-1]
    except Exception:
        return None
    return None

def set_wifi(enabled: bool):
    if not is_admin():
        return False
    iface = _find_wifi_interface()
    if not iface:
        return False
    state = "enable" if enabled else "disable"
    try:
        subprocess.check_call(["netsh", "interface", "set", "interface", iface, state], shell=False)
        return True
    except subprocess.CalledProcessError:
        return False