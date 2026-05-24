#!/usr/bin/env bash
set -euo pipefail

APP_NAME="kitty-discord-rpc"
SERVICE_FILE="$HOME/.config/systemd/user/$APP_NAME.service"

systemctl --user disable --now "$APP_NAME.service" 2>/dev/null || true

rm -f "$SERVICE_FILE"

systemctl --user daemon-reload

echo "Removed $APP_NAME.service"
