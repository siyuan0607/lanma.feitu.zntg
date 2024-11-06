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


"""
{
    "order_book_id": "",  # 标的编号
    "symbol": "",  # 标的简称
    "title": "",  # 正文标题
    "display_content": "", # 展示名称
    "start_date":  "", # 开始日期
    "end_date": "", # 结束日期
    "methods":[] # 分析方法标记，示例：基本面分析、财务面分析
}
"""


def analysis(params: dict):
    resp, code = post('analysis', data=params)
    if code != 200:
        raise Exception(resp)
    data = resp.get("data", [])
    data = json.dumps(data)
    return 200, data


def main():
    params = 入参报文
    params = json.loads(params)
    执行代码, 查询结果 = analysis(params)


main()
