import logging


def not_found_404_view(request):
    return '404 WHAT', '404 PAGE Not Found'


class WebApp:
    def __init__(self, routes={}, front_controllers=[]):
        self.routes = routes
        self.front_controllers = front_controllers

    def __call__(self, environ, start_response):
        logging.debug(type(environ))
        logging.debug(environ)
        tmp_path = environ['PATH_INFO']
        path = tmp_path + '/' if not tmp_path.endswith('/') else tmp_path
        view = self.routes.get(path, not_found_404_view)
        request = {}
        for f_c in self.front_controllers:
            f_c(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
