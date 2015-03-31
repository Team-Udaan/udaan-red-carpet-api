__author__ = 'alay'

from src.basehandler import BaseHandler
from couch import AsyncCouch
from tornado.gen import coroutine


class LoginHandler(BaseHandler):

    @coroutine
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        ip = self.request.remote_ip

        map_function = 'function(doc){if(doc.username == "' + username + '" && doc.ip == "' + ip + '"){emit(null, doc)}}'
        reduce_function = None
        view_doc = dict(map=map_function, reduce=reduce_function)
        client = AsyncCouch('logged_in', self.localhost)
        data = yield client.temp_view(view_doc)
        if data['total_rows'] != 0:
            self.send_error(403)
        else:
            doc = dict()
            doc['username'] = username
            doc['ip'] = ip
            doc['userAgent'] = self.request.headers['User-Agent']
            client.save_doc(doc)
            self.send_error(200)
        client.close()
        return