from main import app
from wsgiref.simple_server import make_server

if __name__ == "__main__":
    httpd = make_server('localhost', 8080, app)
    httpd.serve_forever()
