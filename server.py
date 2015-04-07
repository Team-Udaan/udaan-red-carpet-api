__author__ = 'alay'


from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from src.loginhandler import LoginHandler
from src.votehandler import VoteHandler
from src.feedbackhandler import FeedbackHandler
from src.getfeedbackhandler import GetfeedbackHandler
from src.analyticshandler import AnalyticsHandler
from tornado.options import options, define
from tornado.web import RequestHandler
from tornado.options import parse_command_line


define('ip', default='172.31.40.214', help="run on the given ip", type=str)
parse_command_line()

class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render('index.html')


app = Application([
    (r'/', IndexHandler),
    (r'/api/login', LoginHandler),
    (r'/api/feedback', FeedbackHandler),
    (r'/api/getfeedback', GetfeedbackHandler),
    (r'/api/analytics', AnalyticsHandler),
    (r'/api/vote', VoteHandler)
])

server = HTTPServer(app)
server.listen(8001, address=options.ip)
IOLoop.instance().start()