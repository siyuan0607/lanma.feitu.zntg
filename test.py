import utils, config
from utils import charts
import pandas as pd
import json, logging, os

host = 'http://localhost:5050/rests/'

logger = utils.get_logger(__name__)


def test_http(**kwargs):
    try:
        method = kwargs.get('method')
        url = kwargs.get('url')
        headers = kwargs.get('headers')
        data = kwargs.get('data')
        content_type = headers.get('Content-Type')
        url = host + url
        resp = utils._request(url=url, method=method, headers=headers, content_type=content_type, data=data)
        code = resp.get('code')
        msg = resp.get('msg')
        data = resp.get('data')
        logger.info(f"{kwargs['url']}用例执行成功，code: {code}, msg: {msg}, data: {data}")
        return True
    except Exception as e:
        logger.error(f"{kwargs['url']}用例执行失败，失败原因为：{e}")
        return False


def test_charts():
    logger.info("开始对图表进行测试。")
    logger.info("开始对draw_line_chart进行测试。")
    df = pd.DataFrame({'X': [1, 2, 3, 4, 5], 'Y': [1, 2, 3, 4, 5]})
    image, content_type = charts.draw_line_chart(df, x='X', y='Y', title='测试折线图')
    with open('./images/line_chart.png', 'wb') as file:
        file.write(image)
    logger.info("完成对draw_line_chart进行测试。")
    logger.info("开始对draw_bar_chart进行测试。")
    image, content_type = charts.draw_bar_chart(df, category='X', value='Y', title='测试柱状图')
    with open('./images/bar_chart.png', 'wb') as file:
        file.write(image)
    logger.info("完成对draw_bar_chart进行测试。")
    logger.info("开始对draw_kline_chart进行测试。")
    df = pd.DataFrame({'Date': ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05'],
                       'Open': [30, 40, 50, 60, 70], 'High': [50, 60, 70, 80, 90], 'Low': [10, 20, 30, 40, 50],
                       'Close': [20, 30, 40, 50, 60], 'Volume': [100, 200, 300, 400, 500]})
    image, content_type = charts.draw_kline_chart(df, date='Date', open='Open', high='High', low='Low', close='Close',
                                                  volume='Volume')
    with open('./images/kline_chart.png', 'wb') as file:
        file.write(image)
    logger.info("完成对draw_kline_chart进行测试。")


def main():
    count = 0
    success = 0
    failed = 0
    logger.info("开始进行对rests服务进行检查，开始检索http请求用例。")
    for root, dirs, files in os.walk("./tests"):
        for file in files:
            if file.endswith(".json"):
                count += 1
                logger.info(f"开始对{file}进行测试。")
                with open(os.path.join(root, file), "r") as f:
                    data = json.load(f)
                    flag = test_http(**data)
                    if flag:
                        success += 1
                    else:
                        failed += 1
                logger.info(f"完成对{file}进行测试。")

    logger.info(f"完成进行对rests服务进行检查，总用例数：{count}、通过数：{success}、失败数：{failed}。")
    test_charts()


if __name__ == '__main__':
    main()
