__author__ = 'alay'

from src.basehandler import BaseHandler
import redis
from hashlib import md5


class LoginHandler(BaseHandler):

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')

        client = redis.Redis()
        flag = client.get(username)
        if flag:
            self.send_error(400)
        else:
            password_hash_once = md5(str(username).encode('utf-8')).hexdigest()
            password_hash = md5(password_hash_once.encode('utf-8')).hexdigest()[0:4]
            if password == password_hash:
                with client.pipeline() as pipe:
                    while True:
                        try:
                            pipe.watch('counter')
                            pipe.multi()
                            pipe.set(username, True)
                            pipe.incr('counter')
                            pipe.execute()
                            break
                        except redis.WatchError as error:
                            continue
                self.send_error(200)
            else:
                self.send_error(403)