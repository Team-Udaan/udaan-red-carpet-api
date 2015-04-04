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
        login = data['login']
        feedback = data['feedback']
        client = AsyncCouch('poll-feedback', couch_url='http://admin:admin@localhost:5984')
        doc = dict()
        doc[login['enroll']] = feedback
        print(doc)
        try:
            yield client.save_doc(doc)
            self.response['ok'] = True
        except Exception as error:
            print(error)
            self.response['ok'] = False

        self.send_error(200)