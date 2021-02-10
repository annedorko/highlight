import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler, HTTPServer


class SetDirectory(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = 'site/' + self.path
        super().do_GET()


def run(server_class=HTTPServer, handler_class=SetDirectory):
    server_address = ('', 4242)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
