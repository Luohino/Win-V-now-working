import winreg
import os
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def enable_clipboard_history():
    # Path 1: User level
    user_path = r"Software\Microsoft\Clipboard"
    # Path 2: Policy level (bypasses "managed by organization")
    policy_path = r"SOFTWARE\Policies\Microsoft\Windows\System"
    
    try:
        # 1. Enable for current user
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, user_path)
        winreg.SetValueEx(key, "EnableClipboardHistory", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        print("Successfully enabled Clipboard History for the current user.")

        # 2. Bypass organization policy (requires admin)
        if is_admin():
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, policy_path)
            winreg.SetValueEx(key, "AllowClipboardHistory", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            print("Successfully bypassed organization restrictions (AllowClipboardHistory set to 1).")
        else:
            print("\n[!] WARNING: Could not bypass organization restrictions because the script is not running as Administrator.")
            print("[!] Please right-click your Terminal/PowerShell and select 'Run as Administrator', then run this script again.")

        print("\n[SUCCESS] Registry changes applied.")
        print("Please RESTART your computer for changes to take effect.")
        print("Then try pressing Win + V.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if os.name != 'nt':
        print("This script only works on Windows.")
    else:
        enable_clipboard_history()
