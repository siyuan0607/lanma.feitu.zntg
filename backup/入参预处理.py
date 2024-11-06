import json
from datetime import datetime as pydatetime


def check_params(params):
    order_book_id = params.get("order_book_id", "")
    methods = params.get('methods', [])
    if len(order_book_id) == 0:
        raise Exception(f"未解析到投资标的,{params}")
    if len(methods) == 0:
        raise Exception(f"未解析到分析方法,{params}")

    start = params.get("start_date", "")
    end = params.get("end_date", "")

    # 当没有指定交易日，默认指定为开始日为9月2日，结束日为2024年10月25日
    if len(start) == 0 or len(end) == 0:
        # 获取最近一个交易日
        if len(start) == 0:
            start = pydatetime.strptime("2024-9-2", "%y-%M-%d")
        if len(end) == 0:
            end = pydatetime.strptime("2024-10-25 23:59:59", "%y-%M-%d %H:m:s")

    else:
        start = pydatetime.strftime(start, "%y-%M-%d %H:%m:s")
        end = pydatetime.strftime(end, "%y-%M-%d %H:%m:s")
    if start > end:
        raise Exception(f"入参错误：开始时间不能比结束时间晚。")


def main():
    try:
        input_params = json.loads(入参报文)
        check_params(input_params)
        入参报文 = json.dumps(input_params)
        执行代码 = 200
    except Exception as err:
        执行代码 = 400
        if 调试开关 == "1":
            raise err


main()
