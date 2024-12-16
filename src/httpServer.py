import http.server
from threading import Thread, current_thread
from sys import stderr
from functools import partial
from os.path import abspath


def launchHttpServerInDirectory(port, path):
    print('Launch HTTP Server for localhost and port:' +
          port + ' and path: ' + path)
    httpd, thread = ServeDirectoryWithHTTP(path, int(port))
    return httpd


def stopHttpServer(httpd):
    httpd.shutdown()


def ServeDirectoryWithHTTP(directory=".", port=9000):

    hostname = "localhost"
    directory = abspath(directory)
    handler = partial(_SimpleRequestHandler, directory=directory)
    httpd = http.server.HTTPServer((hostname, port), handler, False)
    # Block only for 0.5 seconds max
    httpd.timeout = 0.5
    # Allow for reusing the address
    httpd.allow_reuse_address = True

    _xprint("server about to bind to port %d on hostname '%s'" %
            (port, hostname))
    httpd.server_bind()

    address = "http://%s:%d" % (httpd.server_name, httpd.server_port)

    _xprint("server about to listen on:", address)
    httpd.server_activate()

    def serve_forever(httpd):
        with httpd:  # to make sure httpd.server_close is called
            _xprint(
                "server about to serve files from directory (infinite request loop):", directory)
            httpd.serve_forever()
            _xprint("server left infinite request loop")

    thread = Thread(target=serve_forever, args=(httpd, ))
    thread.setDaemon(True)
    thread.start()

    return httpd, address


def _xprint(*args, **kwargs):
    """Wrapper function around print() that prepends the current thread name"""
    print("[", current_thread().name, "]",
          " ".join(map(str, args)), **kwargs, file=stderr)


class _SimpleRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Same as SimpleHTTPRequestHandler with adjusted logging."""

    def log_message(self, format, *args):
        """Log an arbitrary message and prepend the given thread name."""
        stderr.write("[ " + current_thread().name + " ] ")
        http.server.SimpleHTTPRequestHandler.log_message(self, format, *args)
