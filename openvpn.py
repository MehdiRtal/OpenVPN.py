import subprocess
import os
import time


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

    def connect(self, profile_path: str, username: str = None, password: str = None, *args):
        if username and password:
            with open("auth.txt", "w") as f:
                f.write(f"{username}\n{password}")
        process = subprocess.Popen([
            self.process,
            "--config",
            os.path.abspath(profile_path),
            "--auth-user-pass" if username and password else None,
            os.path.abspath("auth.txt") if username and password else None,
            "--auth-nocache",
            *args
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            if process.poll():
                raise Exception(process.stderr.read().strip())
            elif "Initialization Sequence Completed" in process.stdout.readline().strip():
                break
        if os.path.exists("auth.txt"):
            os.remove("auth.txt")

    def disconnect(self):
        subprocess.Popen("taskkill /IM openvpn.exe /T /F", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.disconnect()


with OpenVPN() as ovpn:
    ovpn.connect("profile.ovpn", "romanticking95@gmail.com", "ZEEN12345678!@#$")
    print("test")
    time.sleep(120)