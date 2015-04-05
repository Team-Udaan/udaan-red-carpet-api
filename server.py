__author__ = 'alay'


from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from src.loginhandler import LoginHandler
from src.votehandler import VoteHandler
from src.feedbackhandler import FeedbackHandler
from src.basehandler import BaseHandler
from tornado.options import options, define


define("ip", default='192.168.1.111', help="run on the given ip", type=str)


class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')


app = Application([
    (r'/', IndexHandler),
    (r'/api/login', LoginHandler),
    (r'/api/feedback', FeedbackHandler),
    (r'/api/vote', VoteHandler)
])

server = HTTPServer(app)
server.listen(8000, options.ip)
IOLoop.instance().start()