import json


def build_response(data):
    return data.get("msg", "系统异常，请稍后重试！")


def main():
    data = 关键变量
    data = json.loads(data)
    msg = build_response(data)
    最终回复 = msg


main()
