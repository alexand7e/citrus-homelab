#!/bin/bash
echo "========================================="
echo "  POCO HOMELAB - Starting"
echo "========================================="

echo "[1/6] SSH..."
sshd

echo "[2/6] Camera API..."
pkill -f camera-api 2>/dev/null
sleep 1
nohup python3 ~/camera-api.py > /dev/null 2>&1 & disown

echo "[3/6] FileBrowser..."
pkill -f filebrowser 2>/dev/null
sleep 1
nohup ~/filebrowser -d ~/filebrowser.db &>/dev/null &

echo "[4/6] Nginx..."
nginx

echo "[5/6] Syncthing..."
syncthing &

echo "[6/6] Tailscale..."
tailscaled --tun=userspace-networking --socks5-server=localhost:1055 &
sleep 2
tailscale up --accept-routes --accept-dns 2>/dev/null || echo "  Run 'tailscale up' manually"

IP=$(tailscale ip -4 2>/dev/null || ip addr show wlan0 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
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