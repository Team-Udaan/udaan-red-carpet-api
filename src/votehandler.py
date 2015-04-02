__author__ = 'alay'


from src.basehandler import BaseHandler
import json
import redis
from tornado.httputil import HTTPServerRequest


class VoteHandler(BaseHandler):

    def options(self, *args, **kwargs):
        self.send_error(200)

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        login = data['login']

        if BaseHandler.check_credentials(login['enroll'], login['key']):
            self.ok = True
            if login['enroll'] == 130070107003:
                self.voted = True
            else:
                self.voted = False
        else:
            self.ok = False
            self.voted = False

        self.send_error(200)
        return