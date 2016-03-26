__author__ = 'alay'

from src.basehandler import BaseHandler
import json


class LoginHandler(BaseHandler):

    def options(self, *args, **kwargs):
        self.send_error(200)

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        enroll = data['enroll']
        key = data['key']

        if BaseHandler.check_credentials(enroll, key):

            flag = self.client.get(enroll)
            if flag:
                self.response['ok'] = False
                self.response['error'] = []
                self.response['error'].append('voted')
                self.send_error(200)
            else:
                self.response['ok'] = True
                self.send_error(200)
        else:
            self.response['ok'] = False
            self.response['error'] = []
            self.response['error'].append('credentials')
            self.send_error(200)

    def __del__(self):
        del self.client
