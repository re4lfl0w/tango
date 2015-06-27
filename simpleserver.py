from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import Cookie


class MyRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        content = '<html><body>Path is: %s</body></html>' % self.path
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-length', str(len(content)))

        cookie = Cookie.SimpleCookie()
        cookie['id'] = 'some_value_42'

        self.wfile.write(cookie.output())
        self.wfile.write('\r\n')

        self.end_headers()
        self.wfile.write(content)



server = HTTPServer(('', 59900), MyRequestHandler)
server.serve_forever()