from datetime import datetime as pydatetime
from analysis.base import _BaseAnalysis
import services


class _TradeAnalysis(_BaseAnalysis):
    def __init__(self) -> None:
        self.service = services.DataService()
        self.template = """![【股票名称】主力资金流向](【主力资金流向报表url链接】)  
以下是对【股票名称】资金面情况的分析：
#### 主力资金流向分析：
主力资金流向【主力资金情况】亿元，表明近期主力资金以【主力资金流向分析】为主。

#### 融资分析：
从【开始日期】的【开始日期融资额】亿元减少至【结束日期】的【结束日期融资额】亿元。
融资净买入额在【融资净买入额明细】。

#### 北向资金分析：
在【日期区间】的区间内，陆股通净买入额呈现波动状态。

![【股票名称】融资余额和融资净买入额](【融资余额和融资净买入额报表url链接】)  

#### 总结：
【股票名称】在近期的资金面表现显示出一定的波动性。主力资金整体呈现【主力资金流动状态】状态，而融资余额和融资净买入额的波动则表明杠杆资金对【股票名称】的态度也在发生变化。北向资金的动向在最近的数据中并不明确，需要进一步观察。整体来看，【股票名称】的资金面情况较为复杂，投资者应密切关注后续的资金流向和市场动态。
        """
        self.key_dict = {
            "股票名称": None,
            "开始日期": None,
            "结束日期": None,
            "主力资金情况": None,
            "主力资金流向分析": None,
            "开始日期融资额": None,
            "结束日期融资额": None,
            "融资净买入额明细": None,
            "日期区间": None,
            "融资余额和融资净买入额报表url链接": None,
            "主力资金流动状态": None
        }
        super().__init__()

    def execute(self, **kwargs):
        order_book_id = kwargs.get("order_book_id")
        start_date = kwargs.get("start_date")
        end_date = kwargs.get("end_date")
        instrument_info = self.service.get_instruments(keywords=order_book_id)
        start_date = pydatetime.strptime(start_date, "%y-%M-%d %H:%m:s")
        end_date = pydatetime.strptime(end_date, "%y-%M-%d %H:%m:s")
        self.fill_data(instrument_info, start_date=start_date, end_date=end_date)
        result = self.template
        for key, value in self.key_dict.items():
            result = result.replace(f'【{key}】', value)
        return result

    def fill_data(self, instrument_info, start_date, end_date):
        order_book_id = instrument_info.get('order_book_id')
        money_flow = self.service.get_money_flow(order_book_id=order_book_id, start_date=start_date, end_date=end_date)
        self.key_dict['股票名称'] = instrument_info.get('symbol')
        self.key_dict['开始日期'] = start_date.strftime("%M月%d日")
        self.key_dict['结束日期'] = start_date.strftime("%M月%d日")
        buy_sell_diff = money_flow['BUY_VALUE_LARGE_ORDER'].sub(money_flow['SELL_VALUE_LARGE_ORDER']).sum()
        self.key_dict['主力资金情况'] = str(round(buy_sell_diff, 2)) + "万元"
        if buy_sell_diff > 0:
            self.key_dict['主力资金流向分析'] = "流入"
        elif buy_sell_diff < 0:
            self.key_dict['主力资金流向分析'] = "流出"
        else:
            self.key_dict['主力资金流向分析'] = "稳定"
        self.key_dict['开始日期融资额'] = str(round(money_flow['BUY_VALUE_LARGE_ORDER'].sum(), 2)) + "万元"
        self.key_dict['结束日期融资额'] = str(round(money_flow['SELL_VALUE_LARGE_ORDER'].sum(), 2)) + "万元"


    def draw_chart(self):
        pass

    @staticmethod
    def get_name():
        return "交易/资金面分析"
