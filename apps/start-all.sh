#!/bin/bash
echo "========================================="
echo "  POCO HOMELAB - Starting"
echo "========================================="

echo "[1/5] SSH..."
sshd

echo "[2/5] Camera API..."
pkill -f camera-api 2>/dev/null
sleep 1
nohup python3 ~/camera-api.py > /dev/null 2>&1 & disown

echo "[3/5] FileBrowser..."
pkill -f filebrowser 2>/dev/null
sleep 1
nohup ~/filebrowser -d ~/filebrowser.db &>/dev/null &

echo "[4/5] Nginx..."
nginx

echo "[5/5] Syncthing..."
syncthing &

IP=$(ip addr show wlan0 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
echo ""
echo "========================================="
echo "  All services started!"
echo "========================================="
echo "Dashboard: http://$IP:8080"
echo "Camera:    http://$IP:8080/cam/"
echo "Files:     http://$IP:8080/files/"
echo "LensCast:  http://$IP:8080/lenscast/"
echo "SSH:       ssh -i ~/.ssh/citrus -p 8022 u0_a259@$IP"
echo "Tailscale: 100.78.36.89"
echo ""