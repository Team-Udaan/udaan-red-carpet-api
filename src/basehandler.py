import os
from datetime import datetime

from tornado.gen import coroutine
from tornado.web import RequestHandler
from os.path import dirname
from hashlib import md5
import traceback
import json
import redis

__author__ = 'alay'


class BaseHandler(RequestHandler):

    root = dirname(__file__).rstrip('/src')

    @coroutine
    def prepare(self):
        self.db = self.settings["db"].udaanRedCarpet
        try:
            self.body = json.loads(self.request.body.decode())
        except Exception:
            self.body = None
        self.start_time = datetime.now().timestamp()
        request = dict(self.request.__dict__.items())
        headers = dict(self.request.headers.__dict__.items())
        request = dict(
            uri=request["uri"],
            body=self.body,
            headers=headers["_dict"]
        )
        self.log_id = yield self.db.log.insert({"request": request})

    @coroutine
    def on_finish(self):
        end_time = datetime.now().timestamp()
        serve_time = end_time - self.start_time
        yield self.db.log.update({"_id": self.log_id},
                                    {"$set": {"response": self.response,
                                              "serveTime": serve_time,
                                              }})

    @staticmethod
    def get_default_function(enroll):
        return "md5(md5(str(" + enroll + ").encode('utf-8')).digest()).hexdigest()[0:4]"

    @staticmethod
    def get_password(enroll):
        function = os.getenv("HASH_FUNCTION", default=BaseHandler.get_default_function(enroll))
        password = eval(eval(function))
        return password

    def initialize(self):
        self.client = redis.StrictRedis()
        self.response = {}
        self.start_time = float()
        self.log_id = None

    def options(self, *args, **kwargs):
        self.send_error(200)

    @staticmethod
    def check_credentials(enroll, key):
        college_code = str(enroll)[2:5]
        if college_code == '007' or college_code == '008':
            double_hash = BaseHandler.get_password(enroll)

            if double_hash == key:
                return True
            else:
                return False
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
            if (list(self.response.keys()).__len__()) == 0:
                self.response['status'] = status_code
                self.response['message'] = self._reason
            self.set_header('Content-Type', 'application/json')
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Credentials", "false")
            self.set_header("Access-Control-Expose-Headers", "*")
            self.set_header("Access-Control-Allow-Methods", "Post, Options")
            self.set_header("Access-Control-Allow-Headers", "Accept, Content-Type")
            self.finish(json.dumps(self.response))
