__author__ = 'alay'

from src.basehandler import BaseHandler
from tornado_cors import CorsMixin
import redis
from tornado.web import asynchronous


class LoginHandler(CorsMixin, BaseHandler):

    @asynchronous
    def post(self, *args, **kwargs):
        enroll = self.get_argument('enroll')
        key = self.get_argument('key')

        CorsMixin.CORS_ORIGIN = '*'
        CorsMixin.CORS_HEADERS = '*'
        CorsMixin.CORS_METHODS = 'POST, OPTIONS'
        CorsMixin.CORS_EXPOSE_HEADERS = '*'
        CorsMixin.CORS_CREDENTIALS = False

        if BaseHandler.check_credentials(enroll, key):
            self.ok = True
            client = redis.Redis()
            flag = client.get(enroll)
            if flag:
                self.voted = True
                self.send_error(200)
            else:
                self.voted = False
                self.send_error(200)
        else:
            self.ok = False
            self.send_error(200)