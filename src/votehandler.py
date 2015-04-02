__author__ = 'alay'


from src.basehandler import BaseHandler
import json


class VoteHandler(BaseHandler):

    def options(self, *args, **kwargs):
        self.send_error(200)

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        login = data['login']

        if BaseHandler.check_credentials(login['enroll'], login['key']):
            self.response['ok'] = True
        else:
            self.response['ok'] = False

        self.send_error(200)
        return