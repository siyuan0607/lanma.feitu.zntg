import json
import requests

REST_HOST = 'http://localhost:5050/rests/'


def post(url: str, data, headers: dict, content_type: str = 'application/json'):
    headers = headers or {}
    url = REST_HOST + url
    headers['Content-Type'] = content_type
    resp = requests.post(url, data=data, headers=headers)
    resp.raise_for_status()
    if resp.status_code == 200:
        return resp.json(), 200
    else:
        return resp.text, resp.status_code


def complete_entities(key_vars, user_info):
    """
    补充实体
    """
    data = {
        "key_vars": key_vars,
        "user_info": user_info
    }
    result, code = post(url='complete_entities', data=data)
    if code >= 300:
        raise Exception(result)
    code = result.get("code", 400)
    if code < 300:
        luyoubiaoji = "满足要求"
    elif code == 401:
        luyoubiaoji = "缺少要素"
    else:
        luyoubiaoji = "不符合要求"

    return luyoubiaoji, json.dumps(result)


def routing(key_vars, user_info):
    if not key_vars:
        # 当从用户的问题中获取不到任何关键变量，则转向到知识检索中
        luyoubiaoji = 'T0知识检索'
        guanjianbianliang = ''
        return
    else:
        luyoubiaoji, guanjianbianliang = complete_entities(key_vars, user_info)
    关键变量 = guanjianbianliang
    路由标记 = luyoubiaoji


def main():
    try:
        key_vars = 关键变量
        user_info = 使用者信息
        key_vars = json.loads(key_vars)
        user_info = json.loads(user_info)
        routing(key_vars, user_info)
    except Exception as err:
        message = f"关键变量：{key_vars}, 用户信息：{user_info}, 错误信息：{err}"
        raise Exception(message=message)


main()
