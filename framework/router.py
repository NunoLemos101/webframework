import re

from framework.middleware import MiddlewareManager
from framework.request import Request


class Router:

    _middleware_manager = MiddlewareManager()

    def __init__(self):
        self.routes = {}

    def get(self, path: str):
        return self.add_route(path, "GET")

    def post(self, path: str):
        return self.add_route(path, "POST")

    def put(self, path: str):
        return self.add_route(path, "PUT")

    def delete(self, path: str):
        return self.add_route(path, "DELETE")

    def add_route(self, path: str, method: str):
        method = method.upper()
        path_regex = re.sub(r'{(\w+)}', r'(?P<\1>[^/]+)', path)

        if path_regex not in self.routes:
            self.routes[path_regex] = {}

        def decorator(handler):
            self.routes[path_regex][method] = handler
            return handler

        return decorator

    def resolve(self, path: str, method: str):
        method = method.upper()
        for path_regex, methods_dict in self.routes.items():
            match = re.match(f"^{path_regex}$", path)
            if match:
                handler = methods_dict.get(method)
                if handler:
                    return handler, match.groupdict()

        return None, {}

    def handle_request(self, request: Request):
        handler, path_params = self.resolve(request.path, request.method)
        if handler:
            return handler(request, **path_params)
        else:
            return None

    def add_middleware(self, middleware):
        self._middleware_manager.add_middleware(middleware)

    def execute_all_middleware(self, request):
        self._middleware_manager.execute_all(request)

    def execute_all_middleware_after(self, request, response):
        self._middleware_manager.execute_all_after(request, response)
