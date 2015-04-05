__author__ = 'alay'

from src.basehandler import BaseHandler


class AnalyticsHandler(BaseHandler):

    categories = ['styleIcon:female', 'persona:male', 'risingStar', 'artist:female', 'styleIcon:male', 'sportsIcon',
                  'face:male', 'stars', 'artist:male', 'suggestions', 'enroll', 'persona:female', 'face:female']

    def get(self, *args, **kwargs):

        for category in AnalyticsHandler.categories:

            category_list = category.split(':')
            self.response[category_list[0]] = {}
            votes = self.client.hgetall(category)
            print(votes, category)
            if category_list.__len__() == 1:
                for vote in votes:
                    self.response[category_list[0]][vote.decode('utf-8')] = votes[vote].decode('utf-8')
            else:
                for vote in votes:
                    self.response[category_list[0]][category_list[1]] = {}
                    self.response[category_list[0]][category_list[1]][vote.decode('utf-8')] = votes[vote].decode('utf-8')
        self.send_error(200)