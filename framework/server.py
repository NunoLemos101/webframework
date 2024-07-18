import importlib
import inspect
import signal
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

from framework.app import app
from framework.orm.models import Model
from framework.request import Request
from framework.settings import settings


def import_view_modules():
    for module_name in settings.VIEW_FILES:
        importlib.import_module(module_name)


def create_all_tables():
    for module_name in settings.MODEL_FILES:
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Model) and obj is not Model:
                obj.create_table()


def add_middlewares():
    for middleware_path in settings.MIDDLEWARE_CLASSES:
        module_path, class_name = middleware_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        middleware_class = getattr(module, class_name)

        app.add_middleware(middleware_class())


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()

    def handle_request(self):
        content_length = int(self.headers['Content-Length']) if 'Content-Length' in self.headers else 0
        request_body = self.rfile.read(content_length) if content_length > 0 else None

        request = Request(path=self.path, method=self.command, headers=self.headers, body=request_body)

        app.execute_all_middleware(request)

        response = app.handle_request(request)

        if response:
            app.execute_all_middleware_after(request, response)
            response_content = response.to_http_response()
            self.send_response(response_content['status_code'])
            for header, value in response_content['headers'].items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response_content['body'].encode())

            response.post_process(request)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')


def run(port: int = 8000):

    import_view_modules()

    create_all_tables()

    add_middlewares()

    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on port {port}...')

    def signal_handler(sig, frame):
        print('\nShutting down the server...')
        httpd.server_close()
        print('Server stopped.')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        print("Server started")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
