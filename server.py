__author__ = 'alay'


from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from src.loginhandler import LoginHandler
from src.votehandler import VoteHandler


server_ip = "127.0.0.1"

app = Application([
    (r'/api/login', LoginHandler),
    (r'/api/vote', VoteHandler)
])

server = HTTPServer(app)
server.listen(8000, server_ip)
IOLoop.instance().start()