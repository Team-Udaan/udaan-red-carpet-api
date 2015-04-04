__author__ = 'alay'


from src.basehandler import BaseHandler
import json
from couch import AsyncCouch
from tornado.gen import coroutine


class FeedbackHandler(BaseHandler):

    @coroutine
    def post(self, *args, **kwargs):
        print(self.request)
        print(self.request.body)
        data = json.loads(self.request.body.decode('utf-8'))
        print(data)
        enroll = data['login']['enroll']
        feedback = data['feedback']
        client = AsyncCouch('poll-feedback', couch_url='http://admin:admin@localhost:5984')
        doc = dict()
        doc[enroll] = feedback
        print(doc)
        voter_id = self.client.get(enroll)
        voter = 'voter:' + voter_id
        self.client.hset(voter, 'stars', feedback['star'])
        self.client.hset(voter, 'suggestion', feedback['suggestion'])
        try:
            yield client.save_doc(doc)
            self.response['ok'] = True
        except Exception as error:
            print(error)
            self.response['ok'] = False

        self.send_error(200)