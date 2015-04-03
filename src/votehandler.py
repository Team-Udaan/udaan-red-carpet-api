__author__ = 'alay'


from src.basehandler import BaseHandler
import json
import redis


class VoteHandler(BaseHandler):


    @staticmethod
    def vote_counter(data, pipe):
        voter = 'voter:' + str(data['login']['enroll'])
        for data_category in data['form']:
            if isinstance(data['form'][data_category], dict):
                for gender in data['form'][data_category]:
                    category = data_category
                    value = data['form'][data_category][gender]
                    category = category + ':' + gender
                    pipe.hset(voter, category, value)
                    pipe.hincrby(category, value)
                    print(category, pipe.hgetall(category))
            else:
                category = data_category
                value = data['form'][data_category]
                pipe.hincrby(category, value)
                pipe.hset(voter, category, value)
                print(category, pipe.hgetall(category))
        pipe.hincrby(voter, 'voted')
        print(voter, pipe.hgetall(voter))
        pipe.save()
        return

    def options(self, *args, **kwargs):
        self.send_error(200)

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        print(data)
        login = data['login']

        if BaseHandler.check_credentials(login['enroll'], login['key']):

            flag = self.client.hexists('voter:' + login['enroll'], 'voted')

            if flag:
                self.response['ok'] = False
                self.response['error'] = list()
                self.response['error'].append('voted')
            else:
                with self.client.pipeline() as pipe:
                    while 1:
                        try:
                            pipe.watch('counter')
                            pipe.multi()
                            VoteHandler.set_vote(data, pipe)
                            pipe.incr('counter')
                            pipe.execute()
                            break
                        except redis.WatchError as error:
                            continue

            self.response['ok'] = True
        else:
            self.response['ok'] = False
            self.response['error'] = list()
            self.response['error'].append('voted')

        self.send_error(200)
        return

    def __del__(self):
        del self.client