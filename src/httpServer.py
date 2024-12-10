from http.server import HTTPServer, SimpleHTTPRequestHandler
import functools


def launchHttpServerInDirectory(port, path):
    Handler = functools.partial(SimpleHTTPRequestHandler, directory=path)
    httpd = HTTPServer(('localhost', port), Handler)
    httpd.serve_forever()
    return httpd


def stopHttpServer(httpd):
    httpd.shutdown()
