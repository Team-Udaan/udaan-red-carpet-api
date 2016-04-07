import json
import motor
from tornado.gen import coroutine
from tornado.template import Loader
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


define('config', default='sample_api.config', help="give relative or full path of configuration file", type=str)
parse_command_line()

configuration_file_path = options.config
ip, port, web_host = get_data(configuration_file_path)


class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        loader = Loader(".")
        self.write(loader.load("index.html").generate(web_host=web_host))


class DataHandler(RequestHandler):

    @coroutine
    def get(self, *args, **kwargs):
        self.db = self.settings["db"].udaanRedCarpet
        data = yield self.db.config.find_one({})
        del data["_id"]
        self.write("URC_DATA=" + json.dumps(data))

client = motor.MotorClient()

app = Application([
    (r'/', IndexHandler),
    (r'/data.js', DataHandler),
    (r'/api/login', LoginHandler),
    (r'/api/feedback', FeedbackHandler),
    (r'/api/getfeedback', GetfeedbackHandler),
    (r'/api/analytics', AnalyticsHandler),
    (r'/api/test', TestHandler),
    (r'/api/vote', VoteHandler)
], db=client)

server = HTTPServer(app)
server.listen(port)
IOLoop.instance().start()
