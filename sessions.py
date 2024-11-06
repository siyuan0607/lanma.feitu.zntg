from utils import redis as cache
from utils import *
import json

logger = get_logger(__name__)


class UserSessions:
    def __init__(self, user_info):
        self.email = user_info.get('邮箱')
        self.key = f"email:%s:session-key:%s"

    def set(self, key, value):
        key = self.key % (self.email, key)
        value = json.dumps(value)
        cache._set_value(key, value)

    def get(self, key, is_json=True):
        key = self.key % (self.email, key)
        value = cache._get_value(key)
        if not value:
            return None

        return json.loads(value) if is_json else value
