__author__ = 'alay'


from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from src.loginhandler import LoginHandler
from src.votehandler import VoteHandler
from src.feedbackhandler import FeedbackHandler
from tornado.options import options, define


define("ip", default='172.31.40.214', help="run on the given ip", type=str)


app = Application([
    (r'/api/login', LoginHandler),
    (r'/api/feedback', FeedbackHandler),
    (r'/api/vote', VoteHandler)
])

server = HTTPServer(app)
server.listen(8001, options.ip)
IOLoop.instance().start()