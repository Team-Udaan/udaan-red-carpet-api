__author__ = 'alay'

from src.basehandler import BaseHandler


class GetfeedbackHandler(BaseHandler):

    def get(self, *args, **kwargs):
        counter = self.client.get('counter')
        counter = counter.decode('utf-8-')
        self.response['counter'] = counter
        self.response['data'] = {}
        for i in range(0, int(counter)):
            voter = 'voter:' + str(i)
            self.response['data'][voter] = {}
            data = self.client.hgetall(voter)
            for each_data in data:
                key = each_data.decode('utf-8')
                self.response['data'][voter][key] = data[each_data].decode('utf-8')
        self.send_error(200)