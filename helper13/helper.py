'''
Wait for POST from allowed (TODO) IP and allowed (TODO) Themis key
'''

from http.server import BaseHTTPRequestHandler, HTTPServer
import settings


def my_handler(path):
    return bytearray(f"Hello World!, I'm a helper => {path} \n", "utf-8")


class MyHandler(BaseHTTPRequestHandler):
    def check_allowed_ip(self):
        '''
        check if request is from allowed IP
        '''
        if self.client_address[0] not in settings.ALLOWED_HOST:
            self.send_error(403)
            return False
        return True

    def do_GET(self):
        '''
        return 404
        '''
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>404</h1></body></html>")
        return

    def do_POST(self):
        if not self.check_allowed_ip():
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(my_handler(self.path))
        return


httpd = HTTPServer((settings.BIND, settings.PORT), MyHandler)
httpd.serve_forever()
