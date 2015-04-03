__author__ = 'alay'

from src.basehandler import BaseHandler
import redis
import json


class LoginHandler(BaseHandler):

    def options(self, *args, **kwargs):
        self.send_error(200)

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        print(self.request.body)
        enroll = data['enroll']
        key = data['key']

        # if BaseHandler.check_credentials(enroll, key):
        if key == 'pass':
            flag = self.client.hexists('voter:' + str(enroll), 'voted')
            if flag:
                self.response['ok'] = False
                self.response['error'] = list()
                self.response['error'].append('voted')
                self.send_error(200)
            else:
                self.response['ok'] = True
                self.send_error(200)
        else:
            self.response['ok'] = False
            self.response['error'] = list()
            self.response['error'].append('credentials')
            self.send_error(200)

    def __del__(self):
        del self.client