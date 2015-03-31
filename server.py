__author__ = 'alay'


from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from src.iphandler import IPHandler
from src.loginhandler import LoginHandler


server_ip = "127.0.0.1"

app = Application([
    (r'/api/ip', IPHandler),
    (r'/api/login', LoginHandler)
])

server = HTTPServer(app)
server.listen(8000, server_ip)
IOLoop.instance().start()