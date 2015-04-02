__author__ = 'alay'


from src.basehandler import BaseHandler
import json
import redis


class VoteHandler(BaseHandler):

    def post(self, *args, **kwargs):
        login = json.loads(self.get_argument('login'))
        form = json.loads(self.get_argument('form'))
        self.voted = form

        if BaseHandler.check_credentials(login['enroll'], login['key']):
            self.ok = True
        else:
            self.ok = False

        self.send_error(200)
        return