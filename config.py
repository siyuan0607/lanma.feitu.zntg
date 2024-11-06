import os

PORT = 5050

DEBUG = True

mq_config = {
    'host': '',
    'port': 6379,
    'db': 0,
    'password': None
}

oss_config = {
    'endpoint': 'oss-cn-shanghai.aliyuncs.com',
    'bucket_name': 'sales-sh-bucket'
}


def get_access_info():
    """
    获取云访问的信息
    :return:
    """
    access_key_id = os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID']
    access_key_secret = os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
    return access_key_id, access_key_secret
