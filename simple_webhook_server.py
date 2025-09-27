import http.server
import socketserver
import json
import os
from urllib.parse import parse_qs, urlparse

class WebhookHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if parsed_path.path == '/webhook':
            # Handle webhook verification
            mode = query_params.get('hub.mode', [''])[0]
            token = query_params.get('hub.verify_token', [''])[0]
            challenge = query_params.get('hub.challenge', [''])[0]
            
            if mode == 'subscribe' and token == '1285389302894210':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(challenge.encode())
                print(f"✅ Webhook verified! Challenge: {challenge}")
                return
            else:
                # Just return webhook is working for simple GET
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Webhook is working!')
                return
        
        self.send_response(404)
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print(f"📥 Received webhook: {post_data.decode()}")
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            return
            
        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    PORT = 8080
    print(f"🚀 Starting simple webhook server on port {PORT}")
    print(f"📱 Test URL: http://localhost:{PORT}/webhook")
    print(f"🔐 Verify token: 1285389302894210")
    print("📋 Use this with any tunnel service (ngrok, localtunnel, etc.)")
    
    with socketserver.TCPServer(("", PORT), WebhookHandler) as httpd:
        httpd.serve_forever()