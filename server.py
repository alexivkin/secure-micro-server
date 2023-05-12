#!/usr/bin/env python3

import os, stat, ssl, signal, http.server
from base64 import b64decode

# convert dockers sigterm into ctrl-c and catch it in the exception
def handle_sigterm(*args):
    raise KeyboardInterrupt()

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
            if self.headers.get('Authorization') is not None and self.headers.get('Authorization') == 'Basic ' + self.key:
                # if correctly authorized
                filename=os.path.basename(self.path)
                if os.path.isfile(filename) and bool(os.stat(filename).st_mode & stat.S_IXUSR): # if the file is executable
                    ret={'filename':filename}
                    exec(open(filename).read(),globals(),ret) # load the code and run it
                    if ret['error'] == None:    # if worked, return the stream
                        self.send_response(200)
                        self.send_header('Content-type', 'application/octet-stream')
                        self.send_header('Content-Length',len(ret['result']))
                        self.end_headers()
                        self.wfile.write(ret['result'])
                    else:
                        self.send_response(501)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(bytes('Server error:' + ret['error'], 'utf8'))
                else:   # if not executable, return the file
                    http.server.SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.do_AUTHHEAD()
                print('Unauthorized')
                self.wfile.write(bytes('Unauthorized', 'utf8'))
        except Exception as ex:
            print("GET exception ",ex)

    def date_time_string(self, time_fmt='%s'):
        return ''

    def log_message(self, format, *args):
        print("%s - - [%s] %s" % (self.client_address[0],self.log_date_time_string(),format % args))

if __name__ == '__main__':

    signal.signal(signal.SIGTERM, handle_sigterm)

    handler = BasicAuthHandler
    handler.server_version = 'microserver'
    handler.sys_version = '1.1'
    with open('./ba.key', 'r') as file:
        handler.key = file.read().replace('\n', '')

    httpd = http.server.HTTPServer(('0.0.0.0', 8443), handler)
    sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sslcontext.load_cert_chain(certfile="./server.pem", keyfile="./server.key")
    httpd.socket = sslcontext.wrap_socket(httpd.socket, server_side=True)

    try:
        os.chdir('./public')
        print("Listening...")
        httpd.serve_forever()
    except KeyboardInterrupt as ex:
        print('Terminating.')
    except Exception as ex:
        print("Server exception ",ex)
