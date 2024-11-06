# -*- coding: utf-8 -*-
import config as appconfig
import oss2
from oss2.credentials import StaticCredentialsProvider


def _get_auth():
    """
    获取access_key_id和access_key_secret
    :return:
    """
    key, secret = appconfig.get_access_info()
    auth = oss2.ProviderAuth(StaticCredentialsProvider(access_key_id=key, access_key_secret=secret))
    return auth


def upload_file(file_content, object_name):
    """
    上传文件
    :param file_content:
    :param object_name:
    :return:
    """
    # 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
    auth = _get_auth()
    # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    # 填写Bucket名称。
    bucket = oss2.Bucket(auth, appconfig.oss_config["endpoint"], appconfig.oss_config["bucket_name"])
    bucket.put_object(object_name, file_content)


def generate_path(object_name) -> str:
    """
    生成文件访问路径
    :param object_name:
    :return:
    """
    auth = _get_auth()
    bucket = oss2.Bucket(auth, appconfig.oss_config["endpoint"], appconfig.oss_config["bucket_name"])

    # 生成下载文件的签名URL，有效时间为3600秒。
    url = bucket.sign_url('GET', object_name, 3600, slash_safe=True)
    return url
