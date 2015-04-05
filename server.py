__author__ = 'alay'


from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from src.loginhandler import LoginHandler
from src.votehandler import VoteHandler
from src.feedbackhandler import FeedbackHandler
from src.analyticshandler import AnalyticsHandler
from tornado.options import options, define
from tornado.web import RequestHandler


define("ip", default='172.31.40.214', help="run on the given ip", type=str)


class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render('index.html')


app = Application([
    (r'/', IndexHandler),
    (r'/api/login', LoginHandler),
    (r'/api/feedback', FeedbackHandler),
    (r'/api/analytics', AnalyticsHandler),
    (r'/api/vote', VoteHandler)
])

server = HTTPServer(app)
server.listen(8000, options.ip)
IOLoop.instance().start()