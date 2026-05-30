# Kitty Discord RPC

A lightweight Discord Rich Presence tool for Linux terminals on X11.

This project is Kitty-first, but it also includes experimental support for other Linux terminals by detecting the focused X11 window, reading its process information, and showing the current terminal session on Discord.

## Features

* Discord Rich Presence for Linux terminals
* Kitty-first support
* Experimental support for other terminals
* X11 focused-window detection
* Current working directory display
* Optional shortened paths like `~/C/P/project-name`
* Configurable Discord image keys and text
* systemd user service support
* Generic config example, not tied to one distro

## Platform support

This project currently targets Linux on X11.

It uses:

* `xdotool`
* `/proc`
* process inspection through Python
* optional `systemd --user` service

Wayland, Windows, and macOS are not supported yet.

## Supported terminals

Support depends on your terminal and desktop environment, but the default config includes:

* Kitty
* Alacritty
* WezTerm
* Ghostty
* Konsole
* XFCE Terminal
* GNOME Terminal
* xterm
* st
* foot

Kitty is the main target. Other terminals are experimental.

## Requirements

* Linux
* X11
* Discord desktop app
* Python 3
* `xdotool`
* `pypresence`
* `psutil`

On Arch Linux:

```sh
sudo pacman -S --needed python python-pip xdotool
```

On Debian or Ubuntu:

```sh
sudo apt install python3 python3-pip python3-venv xdotool
```

On Fedora:

```sh
sudo dnf install python3 python3-pip xdotool
```

## Installation

Clone the repository:

```sh
git clone git@github.com:YOUR_USERNAME/kitty-discord-rpc.git
cd kitty-discord-rpc
```

Run the install script:

```sh
chmod +x scripts/install.sh
./scripts/install.sh
```

The installer creates a virtual environment, installs the Python dependencies, creates a config file, and installs a systemd user service.

## Configuration

The config file is created at:

```sh
~/.config/terminal-discord-rpc/config.json
```

Edit it:

```sh
nvim ~/.config/terminal-discord-rpc/config.json
```

Example:

```json
{
  "client_id": "YOUR_DISCORD_APPLICATION_CLIENT_ID",
  "update_interval": 5,
  "only_when_terminal_focused": true,

  "details_template": "Using {terminal}",
  "state_template": "{cwd}",

  "large_image": "YOUR_LARGE_IMAGE_KEY",
  "large_text": "Terminal",
  "small_image": "YOUR_SMALL_IMAGE_KEY",
  "small_text": "Linux",

  "shorten_home": true,
  "compact_coding_path": true,

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
    "foot"
  ]
}
```

The image values are Discord Developer Portal asset keys. Replace them with your own uploaded asset names.

If you do not want images, leave the image keys empty:

```json
"large_image": "",
"small_image": ""
```

## Discord application setup

Create an application in the Discord Developer Portal.

Then:

1. Copy the application client ID
2. Put it in `client_id`
3. Upload rich presence assets if you want images
4. Use the uploaded asset names in `large_image` and `small_image`

## Running manually

```sh
source .venv/bin/activate
python src/terminal_discord_rpc.py
```

For fish shell:

```fish
source .venv/bin/activate.fish
python src/terminal_discord_rpc.py
```

## Running with systemd

Start and enable the service:

```sh
systemctl --user enable --now terminal-discord-rpc.service
```

Check status:

```sh
systemctl --user status terminal-discord-rpc.service
```

View logs:

```sh
journalctl --user -u terminal-discord-rpc.service -f
```

Restart after changing the config:

```sh
systemctl --user restart terminal-discord-rpc.service
```

Stop it:

```sh
systemctl --user stop terminal-discord-rpc.service
```

Disable it:

```sh
systemctl --user disable terminal-discord-rpc.service
```

## Uninstalling

Stop and remove the user service:

```sh
./scripts/uninstall.sh
```

Remove the service and local config:

```sh
./scripts/uninstall.sh --purge-config
```

## Notes

This project is designed for Linux terminal workflows on X11.

It is not a general cross-platform Discord RPC tool yet. Wayland support may require a different detection method depending on the compositor.

## License

MIT
