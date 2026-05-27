# Kitty Discord RPC

A lightweight Discord Rich Presence tool for Linux terminals on X11.

This project is Kitty-first, but it also includes experimental support for other Linux terminals by detecting the focused X11 window, reading its process information, and showing the current terminal session on Discord.

## Features

- Discord Rich Presence for Linux terminals
- Kitty-first support
- Experimental support for other terminals
- X11 focused-window detection
- Current working directory display
- Optional shortened paths like `~/C/P/project-name`
- Configurable Discord image keys and text
- systemd user service support
- Generic config example, not tied to one distro

## Platform support

This project currently targets Linux on X11.

It uses:

- `xdotool`
- `/proc`
- process inspection through Python
- optional `systemd --user` service

Wayland, Windows, and macOS are not supported yet.

## Supported terminals

Support depends on your terminal and desktop environment, but the default config includes:

- Kitty
- Alacritty
- WezTerm
- Ghostty
- Konsole
- XFCE Terminal
- GNOME Terminal
- xterm
- st
- foot

Kitty is the main target. Other terminals are experimental.

## Requirements

- Linux
- X11
- Discord desktop app
- Python 3
- `xdotool`
- `pypresence`
- `psutil`

On Arch Linux:

```sh
sudo pacman -S --needed python python-pip xdotool
