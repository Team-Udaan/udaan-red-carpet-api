__author__ = 'alay'

from src.basehandler import BaseHandler


class GetfeedbackHandler(BaseHandler):

    def get(self, *args, **kwargs):
        counter = self.client('counter')
        self.response['counter'] = counter
        self.response['data'] = list()
        for i in range(0, counter):
            self.response['data'].append(self.client.hgetall('voter:' + str(i)))
        self.send_error(200)
