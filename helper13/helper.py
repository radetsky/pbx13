'''
Wait for POST from allowed (TODO) IP and allowed (TODO) Themis key
'''

from http.server import BaseHTTPRequestHandler, HTTPServer


def my_handler(path):
    return bytearray(f"Hello World!, I'm a helper => {path} \n", "utf-8")


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>404</h1></body></html>")
        return

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(my_handler(self.path))
        return


httpd = HTTPServer(("", 8080), MyHandler)
httpd.serve_forever()
