__author__ = 'alay'

from src.basehandler import BaseHandler
import redis


class LoginHandler(BaseHandler):

    def options(self, *args, **kwargs):
        self.send_error(200)

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