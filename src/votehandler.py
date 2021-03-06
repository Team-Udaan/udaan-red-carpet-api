from src.basehandler import BaseHandler
import json
import redis

__author__ = 'alay'


class VoteHandler(BaseHandler):

    @staticmethod
    def vote_counter(data, pipe):
        voter = 'voter:' + data['counter']
        pipe.hset(voter, 'enroll', data['login']['enroll'])
        pipe.set(data['login']['enroll'], data['counter'])
        for data_category in data['form']:
            if isinstance(data['form'][data_category], dict):
                for gender in data['form'][data_category]:
                    category = data_category
                    value = data['form'][data_category][gender]
                    category = category + ':' + gender
                    pipe.hset(voter, category, value)
                    pipe.hincrby(category, value)
            else:
                category = data_category
                value = data['form'][data_category]
                pipe.hincrby(category, value)
                pipe.hset(voter, category, value)
        pipe.save()
        return

    def options(self, *args, **kwargs):
        self.send_error(200)

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        login = data['login']

        if BaseHandler.check_credentials(login['enroll'], login['key']):

            flag = self.client.get(login['enroll'])

            if flag:
                self.response['ok'] = False
                self.response['error'] = []
                self.response['error'].append('voted')
            else:
                with self.client.pipeline() as pipe:
                    while 1:
                        try:
                            counter = self.client.get('counter')
                            data['counter'] = str(counter.decode('utf-8'))
                            pipe.watch('counter')
                            pipe.multi()
                            VoteHandler.vote_counter(data, pipe)
                            pipe.incr('counter')
                            pipe.execute()
                            break
                        except redis.WatchError as error:
                            continue

                self.response['ok'] = True
        else:
            self.response['ok'] = False
            self.response['error'] = []
            self.response['error'].append('credentials')

        self.send_error(200)
        return

    def __del__(self):
        del self.client
