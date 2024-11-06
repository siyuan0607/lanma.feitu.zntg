from services.base import BaseService
from datetime import datetime as pydatetime
import pandas as pd
import utils
import os
import json

_data_set = {}
_init = False

logger = utils.get_logger(__name__)


class MockService(BaseService):
    def __init__(self, mock_path='./mock'):
        global _init
        global _data_set
        if not _init:
            self._init_data_set(_data_set, mock_path)
            _init = True
        super().__init__()

    def _init_data_set(self, data_set, mock_path):
        """
        初始化数据集合
        """
        logger.info(f"开始初始化mock数据集，mock_path={mock_path}")
        # 遍历该文件夹和子文件夹下的csv文件，并转换成dataframe对象
        for root, dirs, files in os.walk(mock_path):
            for file in files:
                if file.endswith('.csv'):
                    self.combine_data(root, data_set)
                    break
        logger.info(f"完成初始化mock数据集，共{len(data_set)}个接口。")

    def combine_data(self, dir, data_set):
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    logger.debug(f"开始读取文件{file_path}")
                    df = pd.read_csv(file_path)
                    func_name = file_path.split('/')[2]
                    if func_name not in data_set:
                        data_set[func_name] = df
                    else:
                        org_df = data_set[func_name]
                        data_set[func_name] = pd.concat([org_df, df], ignore_index=True)
                    logger.debug(f"读取文件{file_path}完成，共{len(df)}行数据")

    def get_instruments(self, keywords: list) -> dict:
        if not keywords or len(keywords) == 0:
            return None

        global _data_set
        result = {}
        for keyword in keywords:
            item = keyword.strip()
            df = _data_set['all_instruments']
            # 从df过滤出order_book_id包含item或symbol包含的数据
            df = df.query('order_book_id.str.contains(@item) | symbol.str.contains(@item)')
            result[item] = None
            if len(df) > 0:
                # 提取df中的第一条数据，并转化为json
                data = df.iloc[0].to_json()
                data = json.loads(data)
                result[item] = data
        return result

    def get_price(self, order_book_id: str, start_date: pydatetime, end_date: pydatetime) -> pd.DataFrame:
        if not order_book_id or not start_date or not end_date:
            raise ValueError("参数不能为空")
        global _data_set
        df = _data_set['get_price'].copy()
        df['date'] = pd.to_datetime(df['date'])
        # 从df中提取符合order_book_id，并且时间在start_date和end_date之间的数据
        df = df.query('order_book_id == @order_book_id & date >= @start_date & date <= @end_date')
        return df

    def current_performance(self, order_book_id, info_date):
        """
        返回最近的财务公告
        """
        if not order_book_id or not info_date:
            raise ValueError("参数不能为空")
        global _data_set
        df = _data_set['current_performance'].copy()
        df['info_date'] = pd.to_datetime(df['info_date'])
        df = df.query('order_book_id == @order_book_id & info_date >= @info_date')
        data = df.iloc[0].to_json()
        return json.loads(data)

    def all_performance(self, order_book_id):
        if not order_book_id:
            raise ValueError("参数不能为空")
        global _data_set
        df = _data_set['current_performance'].copy()
        df['info_date'] = pd.to_datetime(df['info_date'])
        df = df.query('order_book_id == @order_book_id')
        data = df.iloc[0].to_json()
        return json.loads(data)

    def index_indicator(self, order_book_id, date):
        """
        返回股票的估值指标
        """
        if not order_book_id or not date:
            raise ValueError("参数不能为空")
        global _data_set
        df = _data_set['index_indicator'].copy()
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df = df.query('order_book_id in @order_book_id & trade_date >= @date')
        data = df.iloc[0].to_json()
        return json.loads(data)

    def get_pit_financials_ex(self, order_book_id, info_data=None):
        """
        返回股票的财务数据
        """
        if not order_book_id:
            raise ValueError("参数不能为空")
        if not info_data:
            info_data = pydatetime(year=2020, month=1, day=1)
        global _data_set
        df = _data_set['get_pit_financials_ex'].copy()
        df['info_data'] = pd.to_datetime(df['info_data'])
        df = df.query('order_book_id in @order_book_id & info_data >= @info_data')
        data = df.iloc[0].to_json()
        return json.loads(data)

    def get_pit_financials_ex_df(self, order_book_id, info_data=None):
        """
        返回股票的财务数据
        """
        if not order_book_id:
            raise ValueError("参数不能为空")
        if not info_data:
            info_data = pydatetime(year=2020, month=1, day=1)
        global _data_set
        df = _data_set['get_pit_financials_ex'].copy()
        df['info_data'] = pd.to_datetime(df['info_data'])
        df = df.query('order_book_id in @order_book_id & info_data >= @info_data')
        data = df.iloc[0].to_json()
        return json.loads(data)

    def get_stock_news(self, order_book_id: str, start_date: pydatetime, end_date: pydatetime):
        global _data_set
        df = _data_set['get_stock_news'].copy()
        df['atetime'] = pd.to_datetime(df['atetime'])
        # 从df中提取符合order_book_id，并且时间在start_date和end_date之间的数据
        df = df.query('order_book_id == @order_book_id & date >= @start_date & date <= @end_date')
        return df

    def get_money_flow(self, order_book_id: str, trade_date: str, start_date: pydatetime, end_date: pydatetime):
        wind_code = self._transform_code(order_book_id)
        global _data_set
        df = _data_set['get_money_flow'].copy()
        df['TRADE_DT'] = pd.to_datetime(df['TRADE_DT'], format='%Y%m%d')
        df = df.query('S_INFO_WINDCODE == @wind_code & TRADE_DT >= @start_date & TRADE_DT <= @end_date')
        return df

    def get_securities_margin(self, order_book_id:str):
        pass


if __name__ == '__main__':
    service = MockService("../mock")
    print("done")
