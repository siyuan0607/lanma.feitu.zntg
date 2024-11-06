from analysis.base import _BaseAnalysis
from datetime import datetime as pydatetime
import services
import json
import utils
from utils import io
from utils import charts
import pandas as pd


class _StockQuotesAnalysis(_BaseAnalysis):
    def __init__(self) -> None:
        self.service = services.DataService()
        self.key_dict = {
            "股票名称": None,
            "日期": None,
            "收盘价": None,
            "当日的涨跌幅": None,
            "涨跌幅描述": None,
            "行情状况": None,
            "市场表现": None,
            "MACD": None,
            "MACD的判断": None,
            "KDJ": None,
            "KDJ水平": None,
            "KDJ的判断": None
        }
        self.template = """
        ![【股票名称】的行情表现(【行情表现折线图url链接】)
        #### 【股票名称】【日期】的行情：
        最新价：【股票名称】的收盘价为【收盘价】元。
        涨幅：当日的涨跌幅为【当日的涨跌幅】%，这表明【股票名称】在当天的交易中实现了【行情状况】。
        
        #### 市场表现
        【股票名称】在【日期】的市场表现【市场表现】。这种【行情状况】的市场表现可能受到多种因素的影响，包括公司基本面变化、行业动态、市场情绪等。投资者可能会对这种上涨作出反应，但也应考虑市场的波动性和不确定性。
        """
        super().__init__()

    def execute(self, **kwargs):
        order_book_id = kwargs['order_book_id']
        start_date = kwargs['start_date']
        end_date = kwargs['end_date']
        if not (order_book_id and start_date and end_date):
            return
        df = self.service.get_price(order_book_id, start_date, end_date)
        instrument_info = self.service.get_instruments(keywords=order_book_id)
        if not df:
            return
        df = df.sort_values(by='date', ascending=False)
        # 取得最后条数据
        last_row = df.iloc[0]
        last_row = last_row.to_json()
        data = json.loads(last_row)
        df = df.reset_index(drop=True)
        self.fill_data(data, instrument_info, start_date=start_date, end_date=end_date)
        self.draw_chart(df)
        result = self.template
        for key, value in self.key_dict.items():
            result = result.replace(f'【{key}】', value)
        return result

    def fill_data(self, data: dict, instrument_info: dict, start_date: pydatetime, end_date: pydatetime):
        self.key_dict['股票名称'] = instrument_info['symbol']
        if start_date == end_date:
            self.key_dict['日期'] = end_date
        else:
            start_date = start_date.strftime('%m年%d日')
            end_date = end_date.strftime('%m年%d日')
            self.key_dict['日期'] = f'{start_date}到{end_date}之间'
        self.key_dict['收盘价'] = round(data['close'], 2)
        self.key_dict['当日的涨跌幅'] = round((data['close'] - data['pre_close']) / data['pre_close'] * 100, 2)
        if data['close'] > data['pre_close']:
            temp = '上涨'
        elif data['close'] < data['pre_close']:
            temp = '下跌'
        else:
            temp = '平盘'
        # 良好，股价有所上升，涨幅达到了3.75
        self.key_dict['行情状况'] = temp
        if self.key_dict['当日的涨跌幅'] > 0:
            self.key_dict['市场表现'] = '良好，股价有所上升，涨幅达到了' + str(self.key_dict['当日的涨跌幅'])
        elif self.key_dict['当日的涨跌幅'] < 0:
            self.key_dict['市场表现'] = '一般，股价有所下降，跌幅达到了' + str(abs(self.key_dict['当日的涨跌幅']))
        else:
            self.key_dict['市场表现'] = '平盘'

    def draw_chart(self, df):
        """
        绘图报表
        """
        """绘制K线图"""
        image, content_type = charts.draw_kline_chart(df, date='date', open='open', high='high', low='low',
                                                      close='close',
                                                      volume='volume')
        # 将图片留存入oss中
        uid = utils.gen_uid()
        today = pydatetime.today()
        object_name = f"{today.year}/{today.month}/{today.day}/line-{uid}.png"
        io.upload_file(image, object_name)
        url = io.generate_path(object_name)
        self.key_dict["净资产收益折线图url链接"] = url

    @staticmethod
    def get_name():
        return '行情分析'
