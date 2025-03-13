import json,socket,os
class Server:
    def __init__(self):
        self.routes = {}

    def get(self, path):
        def decorator(func):
            self.routes[(path, 'GET')] = func
            return func
        return decorator

    def post(self, path):
        def decorator(func):
            self.routes[(path, 'POST')] = func
            return func
        return decorator

    def delete(self, path):
        def decorator(func):
            self.routes[(path, 'DELETE')] = func
            return func
        return decorator

    def handle_request(self, client):
        request = client.recv(1024).decode('utf-8')
        request_line = request.splitlines()[0]
        method, path, _ = request_line.split()
        body = ""
        headers = request.splitlines()
        content_length = 0
        for header in headers:
            if header.startswith("Content-Length:"):content_length = int(header.split(":")[1].strip())
        if content_length > 0:body = request.splitlines()[-1]

        json_data = {}
        if body:
            try:json_data = json.loads(body)
            except json.JSONDecodeError:json_data = {"error": "Invalid JSON"}

        handler = self.routes.get((path, method))
        if handler:response = handler(json_data)
        else:response = '404 Not Found'

        if isinstance(response, dict):
            response_body = json.dumps(response)
            response_headers = 'Content-Type: application/json\r\n'
        else:
            response_body = response
            response_headers = 'Content-Type: text/html\r\n'

        client.send(b'HTTP/1.1 200 OK\r\n' + response_headers.encode() + b'\r\n')
        client.send(response_body.encode('utf-8'))
        client.close()

    def run(self, host='127.0.0.1', port=8000):
        server = socket.socket()
        server.bind((host, port))
        server.listen(10)
        print(f'Serving on http://{host}:{port}')

        while True:
            client, _ = server.accept()
            self.handle_request(client)

    def template_response(self, file_path, context=None):
        if context is None:context = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:html_content = file.read()
            for key, value in context.items():html_content = html_content.replace(f'{{{{ {key} }}}}', str(value))
            return html_content
        else:return '<h1>404 Not Found</h1>'