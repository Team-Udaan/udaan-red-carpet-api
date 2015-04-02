__author__ = 'alay'

from src.basehandler import BaseHandler
import redis
from hashlib import md5


class LoginHandler(BaseHandler):

    def post(self, *args, **kwargs):
        enroll = self.get_argument('enroll')
        key = self.get_argument('key')

        client = redis.Redis()
        flag = client.get(enroll)
        if flag:
            self.ok = ''
            self.voted = True
            self.send_error(406)
        else:
            self.voted = False
            password_hash_once = md5(str(enroll).encode('utf-8')).hexdigest()
            password_hash = md5(password_hash_once.encode('utf-8')).hexdigest()[0:4]
            if key == password_hash:
                self.ok = True
                self.send_error(200)
            else:
                self.ok = False
                self.send_error(403)