import os
import socketserver
from http.server import SimpleHTTPRequestHandler

class SetDirectory(SimpleHTTPRequestHandler):
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


class HighlightServer:
    def __init__(self):
        self.data = {}
        self.data['httpd'] = None

    def httpd(self):
        return self.data['httpd']

    def run(self):
        handler = SetDirectory
        
        with socketserver.TCPServer(("localhost", 4242), handler) as httpd:
            self.data['httpd'] = httpd
            print("Serving at port 4242...")
            print('\n')
            print('http://localhost:4242')
            print('--------')
            httpd.serve_forever()

            try:
                # Serve forever until Ctrl+C is pressed
                httpd.serve_forever()
            except KeyboardInterrupt:
                # Handle Ctrl+C to ensure proper cleanup
                print("Server shutting down...")
            finally:
                # Close the server
                httpd.server_close()

        