
import urllib.parse
import logging
import os
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler


# Constants
HTTP_PORT = 3000
SOURCE = "./front-init"


class HttpHandler(BaseHTTPRequestHandler):
    """Handles HTTP requests and serves HTML and static files."""

    def do_POST(self):
        """Handles POST requests, reads data, and redirects to the homepage."""
        logging.info(f"Received POST request: {self.path}")
        try:
            data = self.rfile.read(int(self.headers['Content-Length']))
            data_parse = urllib.parse.unquote_plus(data.decode())
            data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
            logging.info(f"Parsed data from form: {data_dict}")
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        except Exception as e:
            logging.error(f"Error processing POST request: {e}")
            self.send_html_file("error.html", 500)

    def do_GET(self):
        """Handles GET requests and serves the corresponding HTML or static files."""
        routes = {
            "/": "index.html",
            "/message.html": "message.html"
        }
        pr_url = urllib.parse.urlparse(self.path)
        html_file = routes.get(pr_url.path)
        if html_file:
            self.send_html_file(html_file)
        elif self.is_static_file(pr_url.path):
            self.send_static(pr_url.path)
        else:
           self.send_html_file("error.html", 404)

    def is_static_file(self, path):
        """Checks if the requested file is a static file based on its extension."""
        static_extensions = [".css", ".js", '.png', '.jpg', '.jpeg', '.gif', '.ico']
        _, ext = os.path.splitext(path)
        return ext in static_extensions

    def send_static(self, path):
        """Serves static files based on the request path."""
        try:
            full_path = os.path.join(SOURCE, path.strip("/"))
            if os.path.exists(full_path):
                self.send_response(200)
                mt = mimetypes.guess_type(path)[0] or 'application/octet-stream'
                self.send_header("Content-type", mt)
                self.end_headers()
                with open(full_path, 'rb') as file:
                    self.wfile.write(file.read())
                logging.info(f"Served static file: {path}")
            else:
                self.send_html_file("error.html", 404)
        except Exception as e:
            logging.error(f"Error serving static file {path}: {e}")
            self.send_html_file("error.html", 500)

    def send_html_file(self, filename, status=200):
        """Serves HTML files and handles errors if the file is not found."""
        try:
            full_path = os.path.join(SOURCE, filename)
            with open(full_path, "rb") as file:
                self.send_response(status)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
            logging.info(f"Served HTML file: {filename}")
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            logging.error(f"File not found: {filename}")
        except Exception as e:
            logging.error(f"Error serving HTML file {filename}: {e}")
            self.send_response(500)
            self.end_headers()


def run_http_server():
    """Starts the HTTP server and listens for incoming requests."""
    server = HTTPServer(("", HTTP_PORT), HttpHandler)
    logging.info(f"HTTP Server running on port {HTTP_PORT}")
    server.serve_forever()