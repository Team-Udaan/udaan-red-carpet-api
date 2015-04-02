__author__ = 'alay'

from tornado.web import RequestHandler
from os.path import dirname
from hashlib import md5
import traceback
import json
from tornado_cors import CorsMixin


class BaseHandler(RequestHandler):

    root = dirname(__file__).rstrip('/app')

    def initialize(self):
        print(self.request)
        self.ok = ''
        self.voted = ''

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
            if self.ok == "" and self.voted == "":
                response['status'] = status_code
                response['message'] = self._reason
            else:
                response['ok'] = self.ok
                response['voted'] = self.voted
            self.set_header('Content-Type', 'application/json')
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Credentials", "false")
            self.set_header("Access-Control-Expose-Headers", "*")
            self.set_header("Access-Control-Allow-Methods", "Post, Options")
            self.set_header("Access-Control-Allow-Headers", "Accept, Content-Type")
            print(response)
            self.finish(json.dumps(response))