from datetime import datetime as pydatetime


class BaseService:
    def get_instruments(self, keywords: list):
        """
        获取股票信息
        :param keywords:
        :return:
        """
        raise NotImplementedError

    def get_price(self, order_book_id: str, start_date: pydatetime, end_date: pydatetime):
        """
        所有交易日股票价格信息(按天更新)
        """
        raise NotImplementedError

    def get_money_flow(self, order_book_id: str, trade_date: str, start_date: pydatetime, end_date: pydatetime):
        """
        获得交易详情
        """
        raise NotImplementedError

    def get_history_finance_performance(self, order_book_id: str, start_date: pydatetime, end_date: pydatetime):
        """
        获得历史财务快报
        """
        raise NotImplementedError

    def get_performance_forecast(self, order_book_id: str, start_date: pydatetime, end_date: pydatetime):
        """
        获得最近的财务预报
        """
        raise NotImplementedError

    def get_pit_financials_ex(self, order_book_id: str, info_date: pydatetime):
        """
        获得财报数据
        """
        raise NotImplementedError

    def get_pit_financials_ex_df(self, order_book_id: str, info_date: pydatetime):
        """
        获得财报数据
        """
        raise NotImplementedError

    def get_block_trade(self, order_book_id: str, start_date: pydatetime, end_date: pydatetime):
        """
        获得大宗交易
        """
        raise NotImplementedError

    def get_securities_margin(self, order_book_id: str, start_date: pydatetime, end_date: pydatetime):
        """
        获得融资融券信息
        """
        raise NotImplementedError

    def get_incentive_plan(self, order_book_id: str, start_date: pydatetime, end_date: pydatetime):
        """
        获取合约股权激励数据
        """
        raise NotImplementedError

    def get_restricted_shares(self, order_book_id: str, start_date: pydatetime, end_date: pydatetime):
        """
        获取股票限售解禁明细数据
        """
        raise NotImplementedError

    def get_audit_opinion(self, order_book_id: str, start_date: pydatetime, end_date: pydatetime):
        """
        获取财务报告审计意见
        """
        raise NotImplementedError

    def get_index_indicator(self, order_book_id: str, start_date: pydatetime, end_date: pydatetime):
        """
        获取指数每日估值指标
        """
        raise NotImplementedError

    def get_stock_news(self, order_book_id: str, start_date: pydatetime, end_date: pydatetime):
        raise NotImplementedError

    def _transform_code(self, order_book_id):
        # 将米筐的order book id转成wind的code
        # 沪市 wind SH;米筐 XSHG，深市 wind SZ;米筐 XSHE
        stock_code, exchange = order_book_id.split('.')
        if exchange == 'XSHG':
            return stock_code + '.SH'
        elif exchange == 'XSHE':
            return stock_code + '.SZ'
        raise Exception(f'未识别的市场:{exchange}')
