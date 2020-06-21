#!/usr/bin/env python3

import os, ssl, http.server
from base64 import b64decode

class BasicAuthHandler(http.server.SimpleHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        try:
            if self.headers.get('Authorization') is None:
                self.do_AUTHHEAD()
                print('No Auth Header')
                self.wfile.write(bytes('Unauthorized', 'utf8'))
            elif self.headers.get('Authorization') == 'Basic ' + self.key:
                http.server.SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.do_AUTHHEAD()
                auth_header = self.headers.get('Authorization')
                if len(auth_header.split(' ')) > 1:
                    print(auth_header.split(' ')[1])
                    print(b64decode(auth_header.split(' ')[1]))
                print('Unauthorized')
                self.wfile.write(bytes('Unauthorized', 'utf8'))
        except Exception as ex:
            print("GET exception ",ex)

    def date_time_string(self, time_fmt='%s'):
        return ''

    def log_message(self, format, *args):
        print("%s - - [%s] %s" % (self.client_address[0],self.log_date_time_string(),format % args))

if __name__ == '__main__':

    handler = BasicAuthHandler
    handler.server_version = 'microserver'
    handler.sys_version = '1.1'
    with open('./ba.key', 'r') as file:
        handler.key = file.read().replace('\n', '')

    httpd = http.server.HTTPServer(('0.0.0.0', 8443), handler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./server.pem', server_side=True)

    try:
        os.chdir('./public')
        httpd.serve_forever()
    except Exception as ex:
        print("Server exception ",ex)
