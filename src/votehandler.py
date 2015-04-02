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
        self.voted = data['form']

        if BaseHandler.check_credentials(login['enroll'], login['key']):
            self.ok = True
        else:
            self.ok = False

        self.send_error(200)
        return