# server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/contact"):
            # vulnerável: reflete input sem sanitização (intencional para demo)
            parsed = urlparse.urlparse(self.path)
            params = urlparse.parse_qs(parsed.query)
            msg = params.get('msg', [''])[0]
            self.send_response(200)
            self.send_header('Content-type','text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"<html><body><h2>Message received:</h2><div>{msg}</div></body></html>".encode('utf-8'))
        else:
            try:
                with open("index.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type','text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content)
            except:
                self.send_response(404)
                self.end_headers()

    def do_POST(self):
        if self.path == "/login":
            length = int(self.headers.get('Content-Length',0))
            data = self.rfile.read(length).decode()
            # não autentica de verdade — só demonstra
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
