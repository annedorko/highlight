import os
import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler, HTTPServer


class SetDirectory(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve from site/ directory
        self.path = 'site/' + self.path
        # Enable pretty urls
        f, ext = os.path.splitext(self.path)
        if ext == '':
            html_path = self.path + '.html'
            if os.path.isfile(html_path):
                self.path = html_path
        # Return file
        super().do_GET()


def run(server_class=HTTPServer, handler_class=SetDirectory):
    server_address = ('', 4242)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
