
from src.basehandler import BaseHandler
import datetime

__author__ = 'alay'


class AnalyticsHandler(BaseHandler):
    categories = ['styleIcon:female', 'persona:male', 'risingStar', 'artist:female', 'styleIcon:male', 'sportsIcon',
                  'face:male', 'artist:male', 'persona:female', 'face:female']

    def get(self, *args, **kwargs):

        for category in AnalyticsHandler.categories:
            data = self.client.hgetall(category)
            vote = {}
            for each_data in data:
                vote[each_data.decode('utf-8')] = int(data[each_data].decode('utf-8'))
            self.response[category] = vote

        time = datetime.datetime.timestamp(datetime.datetime.now())
        counter = self.client.get('counter')
        counter = counter.decode('utf-8')
        self.response['timestamp'] = int(time)
        self.response['counter'] = int(counter)
        self.send_error(200)
