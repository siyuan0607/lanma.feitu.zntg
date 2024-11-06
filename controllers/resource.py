from flask_restful import Resource
from flask import request
from utils import get_logger

logger = get_logger(__name__)


class RestfulResource(Resource):
    def __init__(self):
        self.request = request
        self.sessions = None
        super().__init__()

    def args(self, key, default=None, allow_empty=True):
        if key not in self.request.args and ((not self.request.is_json) or
                                             (
                                                     self.request.is_json and key not in self.request.json)) and key not in self.request.form:
            return default
        if key in self.request.form:
            value = self.request.form[key]
        elif request.is_json and key in request.json:
            value = self.request.json[key]
        else:
            value = self.request.args[key]
        if value == '' and not allow_empty:
            return default
        return value

    def files(self, key):
        if key not in self.request.files:
            return None
        return self.request.files[key]
