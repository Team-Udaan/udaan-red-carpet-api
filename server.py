__author__ = 'alay'


from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from src.loginhandler import LoginHandler
from src.votehandler import VoteHandler
from tornado.options import options, define

define('server_ip', type=str, default='172.31.40.214')


app = Application([
    (r'/api/login', LoginHandler),
    (r'/api/vote', VoteHandler)
])

server = HTTPServer(app)
print(options.server_ip)
server.listen(8000, options.server_ip)
IOLoop.instance().start()