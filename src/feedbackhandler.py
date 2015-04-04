__author__ = 'alay'


from src.basehandler import BaseHandler
import json
from couch import AsyncCouch
from tornado.gen import coroutine


class FeedbackHandler(BaseHandler):

    @coroutine
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        enroll = data['login']['enroll']
        feedback = data['feedback']
        voter_id = str(self.client.get(enroll).decode('utf-8'))
        voter = 'voter:' + voter_id
        try:
            self.client.hset(voter, 'stars', feedback['star'])
            self.client.hset(voter, 'suggestions', feedback['suggestions'])
            self.send_error(200)
        except Exception as error:
            self.send_error(500)
