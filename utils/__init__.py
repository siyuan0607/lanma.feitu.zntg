import logging
import logging.config
import yaml
import requests
import os
from datetime import datetime as pydatetime

from utils.redis import _get_value as get_value
from utils.redis import _set_value as set_value

logging_init = False


def now() -> pydatetime:
    return pydatetime.now()


def md5(s: str) -> str:
    """
    md5加密方法
    :param s:
    :return:
    """
    import hashlib
    hl = hashlib.md5()
    hl.update(s.encode(encoding='utf-8'))
    return hl.hexdigest()


def gen_uid() -> str:
    """
    生成uid
    :return:
    """
    import uuid
    return str(uuid.uuid4()).replace('-', '')


def get(url, **kwargs):
    return _request(url, method='get', **kwargs)


def post(url, **kwargs):
    return _request(url, method='post', **kwargs)


def put(url, **kwargs):
    return _request(url, method='put', **kwargs)


def _request(url, method='get', **kwargs):
    """
    请求实现接口
    :param url:
    :param method:
    :param kwargs:
    :return:
    """
    data = kwargs.get('data', {})
    headers = kwargs.get('headers', {})
    timeout = kwargs.get('timeout', 30)
    content_type = kwargs.get('content_type', 'application/x-www-form-urlencoded')

    try:
        if method == 'get':
            res = requests.get(url, params=data, headers=headers, timeout=timeout)
        else:
            headers['Content-Type'] = content_type
            if method == 'post':
                if content_type.lower() == "application/json":
                    res = requests.post(url, json=data, headers=headers, timeout=timeout)
                else:
                    res = requests.post(url, data=data, headers=headers, timeout=timeout)
            elif method == 'put':
                if content_type.lower() == "application/json":
                    res = requests.put(url, json=data, headers=headers, timeout=timeout)
                else:
                    res = requests.put(url, data=data, headers=headers, timeout=timeout)
            else:
                raise ExternalAPIError('不支持的请求方法')
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ExternalAPIError(f"请求失败: {e}")
    data = res.json()
    return data


def get_logger(name="root") -> logging.Logger:
    """
    获取logger对象
    :param name:
    :return:
    """
    global logging_init
    if not logging_init:
        # 检查是否存在logs文件夹，如果不存在就新建
        if not os.path.exists('./logs'):
            os.mkdir('./logs')
        with open('./logging.yaml', 'r') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        logging_init = True
    return logging.getLogger(name)


class ExternalAPIError(Exception):
    """异常类，用于处理与外部API交互时发生的错误。"""

    def __init__(self, message, status_code=None, error_code=None):
        """
        初始化异常。

        :param message: 描述错误的详细信息字符串。
        :param status_code: HTTP状态码（如果有的话）。
        :param error_code: 外部API特定的错误代码（如果有的话）。
        """
        super().__init__(message)  # 调用基类构造函数，初始化内置Exception
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

    def __str__(self):
        """返回异常的字符串表示形式，包括所有相关错误信息。"""
        error_message = f"Error: {self.message}"
        if self.status_code is not None:
            error_message += f" Status Code: {self.status_code}"
        if self.error_code is not None:
            error_message += f" Error Code: {self.error_code}"
        return error_message
