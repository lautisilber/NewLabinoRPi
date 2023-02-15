from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from typing import Callable
from urllib.parse import urlparse
from os import path, listdir


host_name = '0.0.0.0'#'localhost'
server_port = 8765#8080


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server) -> None:
        super().__init__(request, client_address, server)
    
    def html_response(self, html: str) -> None:
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(html, 'utf-8'))

    def send_redirect(self, location: str):
        self.send_response(301)
        self.send_header('Location', location)
        self.end_headers()
    
    def file_response(self, fname: str) -> None:
        content_type = None
        if fname.endswith('.html'):
            content_type = 'text/html'
        elif fname.endswith('.css'):
            content_type = 'text/css'
        elif fname.endswith('.js'):
            content_type = 'application/javascript'
        elif fname.endswith('.json'):
            content_type = 'application/json'
        elif fname.endswith('.txt'):
            content_type = 'text/plain'
        
        try:
            with open(fname, 'r') as f:
                self.send_response(200)
                if content_type:
                    self.send_header('content_type', content_type)
                self.end_headers()
                file_str = f.read()
                self.wfile.write(bytes(file_str, 'utf-8'))
        except:
            self.send_error(500, f'Could not serve file {fname}')
    
    def serve_directory(self, directory: str) -> bool:
        ''' Returns True if file has been served. False otherwise '''
        # only taking into account shallow directory
        path_split = self.path.split('/')
        if len(path_split) != 2:
            return False
        url_fname = path_split[1]
        for fname in (f for f in listdir(directory) if path.isfile(path.join(directory, f))):
            if fname != url_fname: continue
            local_path = path.join(directory, fname)
            self.file_response(local_path)
            return True
        return False

    def do_GET(self):
        www = 'src/www'
        served = self.serve_directory(www)
        if served: return

        if self.path == '/':
            self.send_redirect('/index.html')
        elif self.path == '/test':
            self.html_response('<h1>Test</h1>')
        else:
            self.send_error(404, 'Not found')
    

class ThreadedHTTPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self._webserver_thread = threading.Thread(target=self.serve_forever, daemon=True)
    
    def run_thread(self) -> None:
        self._webserver_thread.start()
    
    def server_close(self) -> None:
        super().server_close()


def create_web_server() -> ThreadedHTTPServer:
    return ThreadedHTTPServer((host_name, server_port), HTTPRequestHandler)


if __name__ == '__main__':
    httpd = ThreadedHTTPServer((host_name, server_port), HTTPRequestHandler)

    print(f'server on url: {host_name}, and on port: {server_port}')

    httpd.run_thread()

    input('press any key to close server...')

    httpd.server_close()
    print('server stopped')