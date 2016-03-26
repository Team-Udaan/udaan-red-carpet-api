import json
import motor
from tornado.gen import coroutine
from loader import get_data
from src.basehandler import BaseHandler
from src.testhandler import TestHandler
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


define('config', default='api.config', help="give relative or full path of configuration file", type=str)
parse_command_line()

configuration_file_path = options.config
ip, port = get_data()


class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render('index.html')


class DataHandler(BaseHandler):

    mongo_client = motor.MotorClient()

    @coroutine
    def get(self, *args, **kwargs):
        data = yield DataHandler.mongo_client.udaanRedCarpet.config.find_one({})
        del data["_id"]
        self.write("URC_DATA=" + json.dumps(data))


app = Application([
    (r'/', IndexHandler),
    (r'/data.js', DataHandler),
    (r'/api/login', LoginHandler),
    (r'/api/feedback', FeedbackHandler),
    (r'/api/getfeedback', GetfeedbackHandler),
    (r'/api/analytics', AnalyticsHandler),
    (r'/api/test', TestHandler),
    (r'/api/vote', VoteHandler)
])

server = HTTPServer(app)
server.listen(port, address=ip)
IOLoop.instance().start()
