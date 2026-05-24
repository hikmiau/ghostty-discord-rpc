#!/usr/bin/env bash
set -euo pipefail

APP_NAME="kitty-discord-rpc"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SERVICE_DIR/$APP_NAME.service"

mkdir -p "$SERVICE_DIR"

cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Kitty Discord RPC

[Service]
WorkingDirectory=$REPO_DIR
ExecStart=/usr/bin/node index.js
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now "$APP_NAME.service"

echo "Installed and started $APP_NAME.service"
echo "Check status with:"
echo "systemctl --user status $APP_NAME.service"
