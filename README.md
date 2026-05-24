# Kitty Discord RPC

A small Discord Rich Presence app for the Kitty terminal on Linux.

It shows Kitty as your current Discord activity, displays your current project/folder, and pauses automatically when Neovim/Vim RPC is active.

## Features

- Shows Kitty terminal on Discord
- Shows the current project/folder name
- Configurable Discord image assets and hover text
- Uses `.env` for the Discord application/client ID
- Pauses when Neovim/Vim is open so editor RPC can take over
- Optional fish shell integration for real-time directory updates
- Optional systemd user service for auto-starting on login
- Includes a Python check script for troubleshooting

## Preview

Example Discord activity:

```txt
Using Kitty
Project: kitty-discord-rpc
```

With assets like:

```txt
Large image: kitty
Small image: arch
```

## Requirements

- Linux
- Node.js
- npm
- Discord desktop app or Vesktop with Rich Presence support
- Kitty terminal
- Optional: fish shell for live directory updates
- Optional: systemd user service for auto-start

## Installation

Clone the repo:

```bash
git clone git@github.com:hikmiau/kitty-discord-rpc.git
cd kitty-discord-rpc
```

Install dependencies:

```bash
npm install
```

Create your environment file:

```bash
cp .env.example .env
nvim .env
```

Put your Discord application ID inside:

```env
CLIENT_ID=your_discord_application_id_here
```

Do not commit your `.env` file.

## Discord application setup

Go to the Discord Developer Portal and create a new application.

Copy the application ID and put it in `.env`:

```env
CLIENT_ID=your_discord_application_id_here
```

Then upload Rich Presence assets using names that match your `index.js` config.

Example:

```txt
kitty
arch
```

In `index.js`, configure the assets:

```js
const config = {
  details: "Using Kitty",
  fallbackProject: "Terminal",

  largeImageKey: "kitty",
  largeImageText: "Kitty Terminal",

  smallImageKey: "arch",
  smallImageText: "Arch Linux",
};
```

The asset keys must match the names in the Discord Developer Portal.

## Running manually

Run:

```bash
node index.js
```

If it works, your Discord profile should show the Kitty activity.

## Real-time folder/project updates

The RPC reads the current directory from:

```txt
~/.cache/kitty-rpc-pwd
```

If you use fish shell, source the helper script:

```fish
source /path/to/kitty-discord-rpc/scripts/kitty-rpc-pwd.fish
```

For a permanent setup, add it to:

```bash
nvim ~/.config/fish/config.fish
```

Example:

```fish
source ~/Documents/Coding/Projects/kitty-discord-rpc/scripts/kitty-rpc-pwd.fish
```

Now the current project/folder should update when you change directories.

## Systemd user service

To install the service:

```bash
./scripts/install-service.sh
```

Check status:

```bash
systemctl --user status kitty-discord-rpc.service
```

View logs:

```bash
journalctl --user -u kitty-discord-rpc.service -f
```

Stop the service:

```bash
systemctl --user stop kitty-discord-rpc.service
```

Disable auto-start:

```bash
systemctl --user disable kitty-discord-rpc.service
```

Uninstall the service:

```bash
./scripts/uninstall-service.sh
```

## Vim/Neovim RPC override

This RPC checks if Neovim is running.

When `nvim` is open, Kitty RPC pauses so your Vim/Neovim Discord RPC can appear instead.

This avoids the terminal activity overriding the editor activity.

## Troubleshooting

Run the checker:

```bash
python scripts/check.py
```

Common things to check:

```bash
node --version
npm --version
ls /run/user/$(id -u)/discord-ipc-*
systemctl --user status kitty-discord-rpc.service
journalctl --user -u kitty-discord-rpc.service -n 50 --no-pager
```

If Discord IPC does not exist, make sure Discord or Vesktop is open.

If the icon does not appear, make sure the asset key in `index.js` matches the asset name in the Discord Developer Portal.

If the project name does not update, make sure the fish helper script is sourced and that this file exists:

```bash
cat ~/.cache/kitty-rpc-pwd
```

## Repository structure

```txt
kitty-discord-rpc/
|-- .env.example
|-- .gitignore
|-- README.md
|-- index.js
|-- package.json
|-- package-lock.json
|-- scripts/
|   |-- check.py
|   |-- install-service.sh
|   |-- uninstall-service.sh
|   `-- kitty-rpc-pwd.fish
`-- systemd/
    `-- kitty-discord-rpc.service.example
```

## Notes

This is a personal Linux rice utility made for Kitty terminal setups.

The repo version should stay clean and public-safe. Keep your real Discord client ID inside `.env`, which is ignored by Git.

## License

MIT
