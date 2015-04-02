__author__ = 'alay'


from src.basehandler import BaseHandler
import json
from tornado_cors import CorsMixin
from tornado.web import asynchronous
import redis


class VoteHandler(CorsMixin, BaseHandler):

    @asynchronous
    def post(self, *args, **kwargs):

        CorsMixin.CORS_ORIGIN = '*'
        CorsMixin.CORS_HEADERS = '*'
        CorsMixin.CORS_METHODS = 'POST, OPTIONS'
        CorsMixin.CORS_EXPOSE_HEADERS = '*'
        CorsMixin.CORS_CREDENTIALS = False

        login = json.loads(self.get_argument('login'))
        form = json.loads(self.get_argument('form'))
        self.voted = form

        if BaseHandler.check_credentials(login['enroll'], login['key']):
            self.ok = True
        else:
            self.ok = False

        self.send_error(200)
        return