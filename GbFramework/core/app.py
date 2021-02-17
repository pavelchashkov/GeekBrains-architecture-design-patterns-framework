def not_found_404_view(request):
    return '404 WHAT', '404 PAGE Not Found'


class WebApp:
    def __init__(self, routes={}, front_controllers=[]):
        self.routes = routes
        self.front_controllers = front_controllers

    def __call__(self, environ, start_response):
        for k, v in environ.items():
            print(f'{k} - {v}')
        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'
        view = self.routes.get(path, not_found_404_view)
        request = {}
        for f_c in self.front_controllers:
            f_c(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
