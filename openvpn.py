import subprocess
import os
import time
import requests


class OpenVPN:
    def __init__(self):
        path_x64 = os.path.join("C:", os.sep, "Program Files", "OpenVPN", "bin")
        path_x86 = os.path.join("C:", os.sep, "Program Files (x86)", "OpenVPN", "bin")
        if os.path.exists(path_x64):
            self.path = path_x64
        elif os.path.exists(path_x86):
            self.path = path_x86
        else:
            raise Exception("OpenVPN is not installed.")
        self.process = os.path.join(self.path, "openvpn.exe")
        self.ip_adress = requests.get("https://api64.ipify.org/").text

    def connect(self, profile_path: str, username: str = None, password: str = None, retries: int = 60, *args):
        if username and password:
            with open("auth.txt", "w") as f:
                f.write(f"{username}\n{password}")
        subprocess.Popen([
            self.process,
            "--config",
            os.path.abspath(profile_path),
            "--auth-user-pass" if username and password else None,
            os.path.abspath("auth.txt") if username and password else None,
            "--auth-nocache",
            *args
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(retries):
            try:
                if requests.get("https://api64.ipify.org/").text != self.ip_adress:
                    return
                time.sleep(1)
            except:
                pass
        raise Exception("Failed to connect to VPN.")

    def disconnect(self):
        if os.path.exists("auth.txt"):
            os.remove("auth.txt")
        subprocess.Popen("taskkill /IM openvpn.exe /T /F", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.disconnect()