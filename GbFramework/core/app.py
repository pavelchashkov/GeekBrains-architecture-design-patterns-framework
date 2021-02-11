import logging


def not_found_404_view():
    return '404 WHAT', [b'404 PAGE Not Found']


class WebApp:
    def __init__(self, routes):
        self.routes = routes

    def __call__(self, environ, start_response):
        logging.debug(type(environ))
        logging.debug(environ)
        path = environ['PATH_INFO']
        view = self.routes.get(path, not_found_404_view)
        code, body = view()
        start_response(code, [('Content-Type', 'text/html')])
        return body
