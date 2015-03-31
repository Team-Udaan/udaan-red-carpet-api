__author__ = 'alay'


from src.basehandler import BaseHandler


class IPHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.message = self.request.remote_ip
        self.send_error(200)