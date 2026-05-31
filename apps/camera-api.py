#!/usr/bin/env python3
import json, socket, urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

LENSCAST = "http://127.0.0.1:41737"
CAMERA_PORT = 41737
ACTIONS = {"start": True, "stop": False, "toggle": "toggle"}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/camera":
            params = parse_qs(urlparse(self.path).query)
            action = params.get("action", [""])[0]
            if action not in ACTIONS:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "invalid action", "valid": list(ACTIONS.keys())}).encode())
                return
            try:
                payload = json.dumps({"streaming": ACTIONS[action]}).encode()
                req = urllib.request.Request(f"{LENSCAST}/api/control", data=payload, headers={"Content-Type": "application/json"}, method="POST")
                resp = urllib.request.urlopen(req, timeout=5)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"action": action, "status": "ok"}).encode())
            except Exception as e:
                self.send_response(502)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        elif path == "/api/status":
            s = socket.socket()
            s.settimeout(1)
            online = False
            try:
                s.connect(("127.0.0.1", CAMERA_PORT))
                online = True
                s.close()
            except:
                pass
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"camera": "online" if online else "offline"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8082), Handler)
    print("Camera API on http://127.0.0.1:8082")
    server.serve_forever()