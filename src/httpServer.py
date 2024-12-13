from http.server import HTTPServer, SimpleHTTPRequestHandler
import functools


def launchHttpServerInDirectory(port, path):
    print('Launch HTTP Server for localhost and port:' + port)
    Handler = functools.partial(SimpleHTTPRequestHandler, directory=path)
    httpd = HTTPServer(('localhost', int(port)), Handler)
    httpd.serve_forever()
    return httpd


def stopHttpServer(httpd):
    httpd.shutdown()
