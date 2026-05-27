#!/bin/sh

set -eu

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG_DIR="$HOME/.config/terminal-discord-rpc"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SYSTEMD_USER_DIR/terminal-discord-rpc.service"

mkdir -p "$CONFIG_DIR"
mkdir -p "$SYSTEMD_USER_DIR"

if [ ! -f "$CONFIG_DIR/config.json" ]; then
  cp "$PROJECT_DIR/config.example.json" "$CONFIG_DIR/config.json"
  echo "Created config: $CONFIG_DIR/config.json"
else
  echo "Config already exists: $CONFIG_DIR/config.json"
fi

cat >"$SERVICE_FILE" <<EOF
[Unit]
Description=Terminal Discord Rich Presence
After=graphical-session.target

[Service]
Type=simple
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/.venv/bin/python $PROJECT_DIR/src/terminal_discord_rpc.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload

echo "Installed service: $SERVICE_FILE"
echo
echo "Next steps:"
echo "1. Edit your config:"
echo "   nvim $CONFIG_DIR/config.json"
echo
echo "2. Start the service:"
echo "   systemctl --user enable --now terminal-discord-rpc.service"
echo
echo "3. Check logs:"
echo "   journalctl --user -u terminal-discord-rpc.service -f"
