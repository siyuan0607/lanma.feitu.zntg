import time
import logging
import redis
from config import mq_config

logger = logging.getLogger(__name__)

r = redis.Redis(host=mq_config['host'],
                port=mq_config['port'],
                db=mq_config['db'],
                password=mq_config['password'])


def _set_value(key, value):
    logger.info(f"设置redis值，key={key}，value={value}")
    r.set(key, value)


def _get_value(key):
    logger.info(f"获取redis值，key={key}")
    return r.get(key)

