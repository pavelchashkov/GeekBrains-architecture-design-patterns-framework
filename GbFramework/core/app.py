import quopri
from wsgiref.util import setup_testing_defaults
from .singletones import SingletonByName

def not_found_404_view(request):
    return '404 WHAT', '404 PAGE Not Found'

ENV_KEY_PATH_INFO = 'PATH_INFO'
ENV_KEY_REQUEST_METHOD = 'REQUEST_METHOD'
ENV_KEY_QUERY_STRING = 'QUERY_STRING'
ENV_KEY_CONTENT_LENGTH = 'CONTENT_LENGTH'
ENV_KEY_WSGI_INPUT = 'wsgi.input'

class WebApp(metaclass=SingletonByName):
    def __init__(self, name, front_controllers=[]):
        self.name = name
        self.routes = {}
        self.front_controllers = front_controllers
        self.env = None

    def __call__(self, env, start_response):
        setup_testing_defaults(env)
        self.env = env
        
        path = self.env[ENV_KEY_PATH_INFO]
        if not path.endswith('/'):
            path = f'{path}/'

        request_method = self.env[ENV_KEY_REQUEST_METHOD]
        request_data = self.parse_wsgi_input_data(self.get_wsgi_input_data())
        query_string = self.env[ENV_KEY_QUERY_STRING]
        request_params = self.parse_wsgi_query_string(query_string)

        request = {
            'method': request_method,
            'data': request_data,
            'params': request_params
        }
        
        view = self.routes.get(path, not_found_404_view)
        
        for f_c in self.front_controllers:
            f_c(request)
        code, body = view(request)
        
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    
    def add_route(self, url):
        def inner(view):
            self.routes[url] = view
        return inner

    def decode_value(self, val: str) -> str:
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')

    def get_wsgi_input_data(self) -> bytes:
        try:
            content_length = int(self.env.get(ENV_KEY_CONTENT_LENGTH, 0))
        except ValueError:
            content_length = 0
        input_data = self.env[ENV_KEY_WSGI_INPUT].read(content_length)
        return input_data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_wsgi_query_string(data_str)
        return result

    def parse_wsgi_query_string(self, data: str) -> dict:
        result = {}
        if data:
            params = data.split('&')
            for p in params:
                k, v = p.split('=')
                result[k] = self.decode_value(v)
        return result

# Логирующий WSGI-application.
# Такой же, как основной, только для каждого запроса 
# выводит информацию (тип запроса и параметры) в консоль.
class DebugWebApp(WebApp):
    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return super().__call__(env, start_response)

# Фейковый WSGI-application.
# Второй — фейковый (на все запросы пользователя отвечает:
# 200 OK, Hello from Fake).
class FakeWebApp(WebApp):
    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']