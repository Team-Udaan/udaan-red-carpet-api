from src.basehandler import BaseHandler


class TestHandler(BaseHandler):
    def serve(self):
        self.response["ok"] = True
        self.response["status"] = 200
        self.write_error(200)

    def post(self, *args, **kwargs):
        self.serve()

    def get(self, *args, **kwargs):
        self.serve()

    def put(self, *args, **kwargs):
        self.serve()

    def delete(self, *args, **kwargs):
        self.serve()
