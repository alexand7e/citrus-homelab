#!/usr/bin/env python3
import json, subprocess, time, urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

LENSCAST = "http://127.0.0.1:41737"
PKG = "com.opencode.multilensipcam"
STREAM_ACTIONS = {"start": "start", "stop": "stop", "toggle": "toggle"}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/camera":
            params = parse_qs(urlparse(self.path).query)
            action = params.get("action", [""])[0]
            if action == "launch":
                try:
                    subprocess.run(["am", "start", "-n", f"{PKG}/.MainActivity"], capture_output=True, timeout=5)
                    time.sleep(3)
                    self._json(200, {"action": "launch", "status": "ok"})
                except Exception as e:
                    self._json(500, {"error": str(e)})
                return
            if action not in STREAM_ACTIONS:
                self._json(400, {"error": "invalid action", "valid": list(STREAM_ACTIONS.keys()) + ["launch"]})
                return
            try:
                url = f"{LENSCAST}/api/{STREAM_ACTIONS[action]}"
                urllib.request.urlopen(url, timeout=5)
                self._json(200, {"action": action, "status": "ok"})
            except Exception as e:
                self._json(502, {"error": str(e)})
        elif path == "/api/status":
            streaming = False
            app_running = False
            try:
                req = urllib.request.Request(f"{LENSCAST}/api/debug/stream", method="GET")
                resp = urllib.request.urlopen(req, timeout=3)
                data = json.loads(resp.read())
                streaming = data.get("streaming", False)
                app_running = data.get("serverRunning", False)
                mjpeg_clients = data.get("mjpegClients", 0)
                mjpeg_fps = data.get("mjpeg", {}).get("approxReceivedFps", 0)
                self._json(200, {
                    "camera": "streaming" if streaming else "offline",
                    "app": "running" if app_running else "stopped",
                    "fps": round(mjpeg_fps, 1),
                    "clients": mjpeg_clients
                })
            except:
                self._json(200, {"camera": "offline", "app": "stopped", "fps": 0, "clients": 0})
        else:
            self.send_response(404)
            self.end_headers()

    def _json(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8082), Handler)
    print("Camera API on http://127.0.0.1:8082")
    server.serve_forever()