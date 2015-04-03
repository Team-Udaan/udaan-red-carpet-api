__author__ = 'alay'


from src.basehandler import BaseHandler
import json


class VoteHandler(BaseHandler):

    def options(self, *args, **kwargs):
        self.send_error(200)

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        print(data)
        login = data['login']

        if BaseHandler.check_credentials(login['enroll'], login['key']):

            if login['enroll'] == 130070107003:
                self.response['ok'] = False
                self.response['error'] = list()
                self.response['error'].append('voted')
            else:
                self.response['ok'] = True
        else:
            self.response['ok'] = False
            self.response['error'] = list()
            self.response['error'].append('voted')
        self.send_error(200)
        return