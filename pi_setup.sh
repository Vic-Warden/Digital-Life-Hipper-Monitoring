#!/bin/bash

REPO_DIR="/home/hippy/duuseedeewuu36"
VENV_DIR="$REPO_DIR/venv"
SERVICE_FILE="/etc/systemd/system/pam.service"

echo "Starting setup..."

# 0. Stop and remove old systemd service if it exists
if systemctl list-units --type=service --all | grep -q pam.service; then
    echo "Stopping and disabling existing pam.service..."
    sudo systemctl stop pam.service
    sudo systemctl disable pam.service
    sudo rm -f "$SERVICE_FILE"
else
    echo "No existing pam.service found, continuing..."
fi

# 1. Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists."
fi

# 2. Activate virtual environment and install dependencies
echo "Installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
if [ -f "$REPO_DIR/requirements.txt" ]; then
    pip install -r "$REPO_DIR/requirements.txt"
else
    echo "No requirements.txt found, skipping."
fi
deactivate

# 3. Create new systemd service file
echo "Setting up systemd service..."

sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Start PAM Python Script at Boot
After=network.target

[Service]
Type=simple
User=hippy
WorkingDirectory=$REPO_DIR/src/back-end/pam
Environment=PYTHONUNBUFFERED=1
ExecStart=$VENV_DIR/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 4. Enable and start the service
echo "Reloading systemd daemon, enabling and starting pam.service..."
sudo systemctl daemon-reload
sudo systemctl enable pam.service
sudo systemctl start pam.service

echo "Setup complete."