from analysis.base import _BaseAnalysis
from datetime import datetime as pydatetime
from utils import charts
from utils import io
import pandas as pd
import services
import utils

logger = utils.get_logger(__name__)


class _FinanceAnalysis(_BaseAnalysis):
    def __init__(self) -> None:
        self.service = services.DataService()
        self.key_dict = {
            "股票名称": None,
            "净资产收益折线图url链接": None,
            "资产负债合计柱状图url链接": None,

            "ROE": None,
            "收益能力": None,

            "毛利率": None,
            "净利率": None,
            "盈利水平和价格控制水平": None,

            "资产总计（亿元）": None,
            "负债合计（亿元）": None,
            "资产负债率": None,
            "财务结构": None,

            "流动资产（亿元）": None,
            "流动负债（亿元）": None,
            "流动比率": None,
            "短期偿债能力": None,

            "经营活动产生的现金流量净额（亿元）": None,
            "经营活动产生的现金流量": None,
            "投资活动产生的现金流量净额（亿元）": None,
            "投资活动中现金流向": None,
            "筹资活动产生的现金流量净额（亿元）": None,

            "存货周转率": None,
            '应收账款周转率': None,
            '总资产周转率': None,
            '资产运营效率': None,

            '权益乘数': None,
            '公司财务杠杆水平': None,
        }

        self.template = """### 贵州茅台财务状况的分析：
        #### 盈利能力分析：
        * 贵州茅台的ROE（净资产收益率）为【ROE】%，表明公司每单位净资产所产生的收益能力【收益能力】。
        * 毛利率达到【毛利率】%，净利率为【净利率】%，显示出【盈利水平和价格控制水平】。
        ![【股票名称】净资产收益率(【净资产收益折线图url链接】)
        
        #### 资产负债状况分析：
        * 资产总计为【资产总计（亿元）】亿元，负债合计为【负债合计（亿元）】亿元，资产负债率为【资产负债率】%，表明公司财务结构【财务结构】。
        * 流动资产为【流动资产（亿元）】亿元，流动负债为【流动负债（亿元）】亿元，流动比率【流动比率】，表明短期偿债能力【短期偿债能力】。
        
        ![【股票名称】资产负债合计(【资产负债合计柱状图url链接】)
        
        #### 现金流量分析：
        * 经营活动产生的现金流量净额为【现金流量净额（亿元）】亿元，显示公司经营活动产生的现金流量【经营活动产生的现金流量】。
        * 投资活动产生的现金流量净额为【投资活动产生的现金流量净额（亿元）】亿元，表明公司在投资活动中现金【投资活动中现金流向】。
        * 筹资活动产生的现金流量净额为【筹资活动产生的现金流量净额（亿元）】亿元，可能与公司偿还债务或分红有关。
        
        #### 财务结构与杠杆分析：
        * 资产负债率为【资产负债率】%，权益乘数为【权益乘数】，表明公司财务杠杆【公司财务杠杆水平】"""
        super().__init__()

    def execute(self, **kwargs):
        order_book_id = kwargs.get("order_book_id", None)
        if not order_book_id:
            raise Exception("order_book_id is required")
        end_date = kwargs.get("end_date", None)
        if not end_date:
            raise Exception("end_date is required")
        end_date = pydatetime.strptime(end_date, "%y-%M-%d %H:%m:s")

        instrument_info = self.service.get_instruments(keywords=order_book_id)
        current_performance = self.service.current_performance(order_book_id, end_date)
        finance_data = self.service.get_pit_financials_ex(order_book_id, end_date)

        self.fill_data(instrument_info=instrument_info, current_performance=current_performance,
                       finance_data=finance_data)
        self.draw_chart(order_book_id)
        result = self.template
        for key, value in self.key_dict.items():
            result = result.replace(f'【{key}】', value)
        return result

    def fill_data(self, finance_data: dict, current_performance: dict, instrument_info: dict):
        """
        填充数据
        """
        """part 1"""
        self.key_dict["股票名称"] = instrument_info.get("symbol")
        self.key_dict["ROE"] = current_performance.get("roe")
        if self.key_dict["ROE"] > 0.15:
            self.key_dict["收益能力"] = '较强'
        elif self.key_dict["ROE"] > 0.05:
            self.key_dict["收益能力"] = '中等'
        else:
            self.key_dict["收益能力"] = '较弱'

        """part 2"""
        self.key_dict["毛利率"] = finance_data.get('gross_profit') / finance_data.get("operating_revenue")
        self.key_dict["净利率"] = finance_data.get('net_profit') / finance_data.get("operating_revenue")
        if self.key_dict["毛利率"] > 0.6:
            if self.key_dict["净利率"] > 0.3:
                self.key_dict["盈利水平和价格控制水平"] = "盈利水平和价格控制水平强"
            elif self.key_dict["净利率"] > 0.1:
                self.key_dict["盈利水平和价格控制水平"] = "盈利水平强，价格控制水平中等"
            else:
                self.key_dict["盈利水平和价格控制水平"] = "盈利水平弱，价格控制水平弱"
        elif self.key_dict["毛利率"] > 0.2:
            if self.key_dict["净利率"] > 0.1:
                self.key_dict["盈利水平和价格控制水平"] = "盈利水平强，价格控制水平弱"
            elif self.key_dict["净利率"] > 0:
                self.key_dict["盈利水平和价格控制水平"] = "盈利水平弱，价格控制水平中等"
            else:
                self.key_dict["盈利水平和价格控制水平"] = "盈利水平弱，价格控制水平弱"
        else:
            self.key_dict["盈利水平和价格控制水平"] = "盈利水平弱，价格控制水平弱"

        """part 3"""
        self.key_dict["资产总计（亿元）"] = round((finance_data.get('current_assets') + finance_data.get(
            'total_fixed_assets') + finance_data.get('non_current_assets')) / 100000000, 2)
        self.key_dict["负债合计（亿元）"] = round(finance_data.get('total_liabilities') / 100000000, 2)
        self.key_dict["资产负债率"] = self.key_dict["负债合计（亿元）"] / self.key_dict["资产总计（亿元）"] * 100
        if self.key_dict["资产负债率"] < 30:
            self.key_dict["财务结构"] = "不够灵活"
        elif self.key_dict["资产负债率"] < 60:
            self.key_dict["财务结构"] = "比较稳健"
        else:
            self.key_dict["财务结构"] = "较差"

        """part 4"""
        self.key_dict["流动资产（亿元）"] = round(finance_data.get('current_assets') / 100000000, 2)
        self.key_dict["流动负债（亿元）"] = round(finance_data.get('current_liabilities') / 100000000, 2)
        self.key_dict["流动比率"] = round(
            finance_data.get('current_assets') / finance_data.get('current_liabilities'), 2)
        self.key_dict["短期偿债能力"] = '较强' if self.key_dict["流动比率"] >= 1 else '较弱'

        """part 5"""
        self.key_dict["经营活动产生的现金流量净额（亿元）"] = round(
            finance_data.get('cash_flow_from_operating_activities') / 100000000, 2)
        self.key_dict["经营活动产生的现金流量"] = finance_data.get('cash_from_operating_activities')
        self.key_dict["投资活动产生的现金流量净额（亿元）"] = round(
            finance_data.get('cash_flow_from_investing_activities') / 100000000, 2)
        self.key_dict["投资活动中现金流向"] = '流入' if self.key_dict["投资活动产生的现金流量净额（亿元）"] < 0 else '流出'
        self.key_dict["筹资活动产生的现金流量净额（亿元）"] = round(
            finance_data.get('cash_flow_from_financing_activities') / 100000000, 2)

        """part 6
        self.key_dict["存货周转率"] = ""
        self.key_dict["应收账款周转率"] = ""
        self.key_dict["总资产周转率"] = ""
        self.key_dict["资产运营效率"] = ""
        """

        """part 7"""
        self.key_dict["权益乘数"] = 1 / (1 - self.key_dict['资产负债率'])
        self.key_dict["公司财务杠杆水平"] = "较低" if self.key_dict["权益乘数"] < 2 else "较高"

    def draw_chart(self, order_book_id):
        """
        绘图报表
        """
        symbol = self.key_dict["股票名称"]
        df = self.service.get_pit_financials_ex_df(order_book_id)
        # 将df中的quarter中的q1转成3月31日，q2转成6月30日，q3转成9月30日，q4转成12月31日
        df['quarter'] = df['quarter'].apply(lambda x: x.replace('q1', '年3月31日').replace('q2', '年6月30日').replace(
            'q3', '年9月30日').replace('q4', '年12月31日'))
        df['quarter'] = pd.to_datetime(df['quarter'])

        """绘制折线图"""
        df['roe'] = df['net_profit'] / df['total_equity'] * 100
        df['gross_margin_ratio'] = df['gross_profit'] / df['operating_revenue']
        df['net_profit_margin_ratio'] = df['net_profit'] / df['operating_revenue']
        image, content_type = charts.draw_line_chart(df, x='quarter', x_label='日期', ys={
            "净资产收益率（roe）": "roe",
            "销售毛利率": "gross_margin_ratio",
            "销售净利率": "net_profit_margin_ratio",
        }, title='')
        # 将图片留存入oss中
        uid = utils.gen_uid()
        today = pydatetime.today()
        object_name = f"{today.year}/{today.month}/{today.day}/line-{uid}.png"
        io.upload_file(image, object_name)
        url = io.generate_path(object_name)
        self.key_dict["净资产收益折线图url链接"] = url

        """绘制柱状报表"""
        df['total_assets'] = str(df['total_assets'] / 100000000) + '亿元'
        df['total_liabilities'] = str(df['total_liabilities'] / 100000000) + '亿元'
        image, content_type = charts.draw_bar_chart(df, x_label='', y_label='', ys={
            "资产总计": "total_assets",
            "负债合计": "total_liabilities",
        }, title=f'{symbol}的资产与负债状况')
        # 将图片留存入oss中
        uid = utils.gen_uid()
        today = pydatetime.today()
        object_name = f"{today.year}/{today.month}/{today.day}/bar-{uid}.png"
        io.upload_file(image, object_name)
        url = io.generate_path(object_name)
        self.key_dict["资产负债合计柱状图url链接"] = url

    @staticmethod
    def get_name():
        return '财务面分析'
