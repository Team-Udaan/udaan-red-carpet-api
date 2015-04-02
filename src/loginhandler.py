__author__ = 'alay'

from src.basehandler import BaseHandler
from tornado_cors import CorsMixin
import redis
from tornado.web import asynchronous


class LoginHandler(CorsMixin, BaseHandler):

    CORS_ORIGIN = '*'
    CORS_HEADERS = '*'
    CORS_METHODS = 'POST, OPTIONS'
    CORS_EXPOSE_HEADERS = '*'
    CORS_CREDENTIALS = False

    def post(self, *args, **kwargs):
        enroll = self.get_argument('enroll')
        key = self.get_argument('key')

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