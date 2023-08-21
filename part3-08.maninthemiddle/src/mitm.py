import http.server as hs
import requests
import sys


class Mitm(hs.BaseHTTPRequestHandler):

    remote_address = None # domain name to connect

    def do_GET(self):
        r = requests.get(self.remote_address + self.path)
        print(r.status_code)
        self.send_response(r.status_code)
        for key in r.headers:
            print(key, r.headers[key])
            self.send_header(key, r.headers[key])
        self.end_headers()
        content = r.content
        if r.headers['Content-type'] == 'text/html':
            content = content.upper()
        #self.wfile.write() # write requires byte array
        self.wfile.write(content) # write requires byte array


def start_server(local_port, remote_address):
    Mitm.remote_address = remote_address
    server = hs.HTTPServer(("localhost", local_port), Mitm)
    server.serve_forever()


# This makes sure the main function is not called immediately
# when TMC imports this module
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('usage: python %s local_port remote_address' % sys.argv[0])
    else:
        start_server(int(sys.argv[1]), sys.argv[2])
