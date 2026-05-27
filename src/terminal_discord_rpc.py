#!/usr/bin/env python3

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any

import psutil
from pypresence import Presence


DEFAULT_CONFIG: dict[str, Any] = {
    "client_id": "",
    "update_interval": 5,
    "only_when_terminal_focused": True,
    "details_template": "Using {terminal}",
    "state_template": "{cwd}",
    "large_image": "",
    "large_text": "Terminal",
    "small_image": "",
    "small_text": "Linux",
    "shorten_home": True,
    "compact_coding_path": True,
    "terminal_names": [
        "kitty",
        "alacritty",
        "wezterm-gui",
        "ghostty",
        "konsole",
        "xfce4-terminal",
        "gnome-terminal",
        "gnome-terminal-server",
        "xterm",
        "st",
        "foot",
    ],
}


def load_config() -> dict[str, Any]:
    config_path = Path.home() / ".config" / "terminal-discord-rpc" / "config.json"
    config = DEFAULT_CONFIG.copy()

    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as file:
            user_config = json.load(file)
            config.update(user_config)

    return config


def run_command(command: list[str]) -> str | None:
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.SubprocessError:
        return None


def get_active_window_pid() -> int | None:
    window_id = run_command(["xdotool", "getactivewindow"])

    if not window_id:
        return None

    pid = run_command(["xdotool", "getwindowpid", window_id])

    if not pid or not pid.isdigit():
        return None

    return int(pid)


def normalize_process_name(name: str) -> str:
    process_name = name.lower()

    aliases = {
        "kitty": "Kitty",
        "alacritty": "Alacritty",
        "wezterm-gui": "WezTerm",
        "ghostty": "Ghostty",
        "konsole": "Konsole",
        "xfce4-terminal": "XFCE Terminal",
        "gnome-terminal": "GNOME Terminal",
        "gnome-terminal-server": "GNOME Terminal",
        "xterm": "xterm",
        "st": "st",
        "foot": "foot",
    }

    return aliases.get(process_name, name)


def is_terminal_process(process: psutil.Process, terminal_names: list[str]) -> bool:
    try:
        process_name = process.name().lower()
    except psutil.Error:
        return False

    return process_name in terminal_names


def find_terminal_process(
    process: psutil.Process,
    terminal_names: list[str],
) -> psutil.Process | None:
    try:
        if is_terminal_process(process, terminal_names):
            return process

        parent = process.parent()

        while parent is not None:
            if is_terminal_process(parent, terminal_names):
                return parent

            parent = parent.parent()

    except psutil.Error:
        return None

    return None


def find_best_cwd(process: psutil.Process) -> str | None:
    candidates: list[psutil.Process] = []

    try:
        candidates.append(process)
        candidates.extend(process.children(recursive=True))
    except psutil.Error:
        pass

    for candidate in reversed(candidates):
        try:
            cwd = candidate.cwd()

            if cwd and os.path.exists(cwd):
                return cwd

        except psutil.Error:
            continue

    return None


def shorten_path(path: str, config: dict[str, Any]) -> str:
    home = str(Path.home())

    if config.get("shorten_home", True) and path.startswith(home):
        path = "~" + path[len(home) :]

    if config.get("compact_coding_path", True):
        path = path.replace("~/Coding/Projects/", "~/C/P/")

    return path


def get_terminal_info(config: dict[str, Any]) -> dict[str, str] | None:
    pid = get_active_window_pid()

    if pid is None:
        return None

    try:
        active_process = psutil.Process(pid)
    except psutil.Error:
        return None

    terminal_process = find_terminal_process(
        active_process,
        config["terminal_names"],
    )

    if terminal_process is None:
        return None

    cwd = find_best_cwd(terminal_process)

    if cwd is None:
        cwd = str(Path.home())

    terminal_name = normalize_process_name(terminal_process.name())

    return {
        "terminal": terminal_name,
        "cwd": shorten_path(cwd, config),
    }


def connect_rpc(client_id: str) -> Presence:
    rpc = Presence(client_id)
    rpc.connect()
    return rpc


def is_placeholder(value: str) -> bool:
    return value.startswith("YOUR_") or value.strip() == ""


def build_payload(
    config: dict[str, Any],
    info: dict[str, str],
    start_time: int,
) -> dict[str, Any]:
    details = config["details_template"].format(**info)
    state = config["state_template"].format(**info)

    payload: dict[str, Any] = {
        "details": details,
        "state": state,
        "start": start_time,
    }

    large_image = str(config.get("large_image", ""))
    large_text = str(config.get("large_text", ""))
    small_image = str(config.get("small_image", ""))
    small_text = str(config.get("small_text", ""))

    if not is_placeholder(large_image):
        payload["large_image"] = large_image

    if large_text.strip():
        payload["large_text"] = large_text

    if not is_placeholder(small_image):
        payload["small_image"] = small_image

    if small_text.strip():
        payload["small_text"] = small_text

    return payload


def main() -> None:
    config = load_config()

    client_id = str(config.get("client_id", ""))

    if is_placeholder(client_id):
        print("Missing Discord client_id.")
        print("Create ~/.config/terminal-discord-rpc/config.json first.")
        return

    rpc: Presence | None = None
    last_payload: dict[str, Any] | None = None
    start_time = int(time.time())

    while True:
        try:
            if rpc is None:
                rpc = connect_rpc(client_id)
                print("Connected to Discord RPC.")

            info = get_terminal_info(config)

            if info is None:
                if config.get("only_when_terminal_focused", True):
                    if last_payload is not None:
                        rpc.clear()
                        last_payload = None
                        print("Cleared RPC because no supported terminal is focused.")

                    time.sleep(config["update_interval"])
                    continue

                info = {
                    "terminal": "Terminal",
                    "cwd": "~",
                }

            payload = build_payload(config, info, start_time)

            if payload != last_payload:
                rpc.update(**payload)
                last_payload = payload
                print(f"Updated RPC: {payload.get('details')} | {payload.get('state')}")

        except KeyboardInterrupt:
            if rpc is not None:
                rpc.clear()

            print("Stopped.")
            return

        except Exception as error:
            print(f"RPC error: {error}")
            rpc = None
            last_payload = None
            time.sleep(10)

        time.sleep(config["update_interval"])


if __name__ == "__main__":
    main()
