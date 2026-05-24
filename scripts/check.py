#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess
import os

HOME = Path.home()
PROJECT = Path(__file__).resolve().parent.parent

checks = []

def add_check(name, ok, note=""):
    status = "OK" if ok else "FAIL"
    checks.append((status, name, note))

add_check("node installed", shutil.which("node") is not None)
add_check("npm installed", shutil.which("npm") is not None)
add_check(".env exists", (PROJECT / ".env").exists(), "create it from .env.example")
add_check("node_modules exists", (PROJECT / "node_modules").exists(), "run npm install")
add_check("package.json exists", (PROJECT / "package.json").exists())
add_check("index.js exists", (PROJECT / "index.js").exists())

ipc_files = list(Path(f"/run/user/{os.getuid()}").glob("discord-ipc-*"))
add_check("Discord IPC found", len(ipc_files) > 0, "open desktop Discord/Vesktop first")

service = HOME / ".config/systemd/user/kitty-discord-rpc.service"
add_check("systemd user service exists", service.exists(), "run scripts/install-service.sh")

pwd_file = HOME / ".cache/kitty-rpc-pwd"
add_check("kitty rpc pwd cache exists", pwd_file.exists(), "source scripts/kitty-rpc-pwd.fish in fish config")

print("Kitty Discord RPC check\n")

for status, name, note in checks:
    line = f"[{status}] {name}"
    if note and status == "FAIL":
        line += f" - {note}"
    print(line)

print("\nService status:")
try:
    subprocess.run(
        ["systemctl", "--user", "status", "kitty-discord-rpc.service", "--no-pager"],
        check=False,
    )
except FileNotFoundError:
    print("systemctl not found")
