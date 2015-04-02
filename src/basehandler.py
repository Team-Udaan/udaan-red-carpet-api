__author__ = 'alay'

from tornado.web import RequestHandler
from os.path import dirname
from hashlib import md5
import traceback
import json


class BaseHandler(RequestHandler):

    root = dirname(__file__).rstrip('/app')
    localhost = 'http://admin:admin@127.0.0.1:5984/'

    def initialize(self):
        self.ok = ''
        self.voted = ''
        self.localhost = 'http://admin:admin@127.0.0.1:5984'

    def options(self, *args, **kwargs):
        self.send_error(200)

    @staticmethod
    def check_credentials(enroll, key):
        key_hash = md5(str(enroll).encode('utf-8')).hexdigest()
        double_hash = md5(key_hash.encode('utf-8')).hexdigest()[0:4]

        if double_hash == key:
            return True
        else:
            return False

    def write_error(self, status_code, **kwargs):
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'application/json')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            response = dict()
            response['ok'] = self.ok
            response['voted'] = self.voted
            # response['message'] = self.message
            self.set_header('Content-Type', 'application/json')
            self.set_header('Access-Control-Allow-Origin', '*')
            self.set_header('Access-Control-Request-Method', 'OPTIONS')
            self.set_header('Access-Control-Request-Method', 'POST')
            self.finish(json.dumps(response))