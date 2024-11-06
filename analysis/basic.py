from analysis.base import _BaseAnalysis
from datetime import datetime as pydatetime
import utils
import services
from utils import io, charts

logger = utils.get_logger(__name__)


class _BasicAnalysis(_BaseAnalysis):
    def __init__(self) -> None:
        self.service = services.DataService()
        self.key_dict = {
            "股票名称": None,
            "所属行业": None,
            "营业收入": None,
            "净利润": None,
            "K线图url链接": None,
            "营业收入同比增长": None,
            "净利润同比增长": None,
            "经营情况整体判断": None,
            "ROE": None,
            "资产净利率": None,
            "销售净利润": None,
            "销售毛利率": None,
            "公司盈利情况判断": None,
            "PE": None,
            "PB": None,
            "市盈率行业排名": None,
            "市净率行业排名": None,
            "估值水平": None
        }

        self.template = """![【股票名称】K线图](【K线图url链接】)
    ### 基本面分析
    【股票名称】作为大陆主板的【所属行业】行业上市公司，其基本面具体分析如下：
    * 营业收入和净利润增长方面，【股票名称】的营业收入为【营业收入】亿元，同比增长【营业收入同比增长】，净利润为【净利润】亿元，同比增长【净利润同比增长】，这表明公司业绩【经营情况整体判断】。
    * 在盈利能力方面，【股票名称】净资产收益率（ROE）为【ROE】，资产净利率为【资产净利率】，销售净利率为【销售净利率】，销售毛利率为【销售毛利率】，显示公司盈利能力【公司盈利情况判断】。
    """
        super().__init__()

    def execute(self, **kwargs):
        order_book_id = kwargs.get("order_book_id", None)
        if not order_book_id:
            raise Exception("order_book_id is required")
        start_date = kwargs.get("start_date", None)
        end_date = kwargs.get("end_date", None)
        if not start_date or not end_date:
            raise Exception("start_date & end_date is required")
        start_date = pydatetime.strptime(start_date, "%y-%M-%d %H:%m:s")
        end_date = pydatetime.strptime(end_date, "%y-%M-%d %H:%m:s")

        self.fill_instrument_info(order_book_id)
        self.fill_kline_chart(order_book_id, start_date, end_date)
        self.fill_finance_performance(order_book_id, end_date)
        self.fill_profit_performance(order_book_id, end_date)
        self.fill_indicator_info(order_book_id, end_date)
        result = self.template
        for key, value in self.key_dict.items():
            result = result.replace(f'【{key}】', value)
        return result

    def fill_indicator_info(self, order_book_id, end_date):
        """
        填充股票指标
        """
        # 无对应指标支持，暂不实现
        return

    def fill_profit_performance(self, order_book_id, end_date):
        """
        填充利润表现明细
        """
        data = self.service.current_performance(order_book_id, end_date)
        self.key_dict['ROE'] = data.get("roe")
        total_assets = data.get('total_assets')
        total_assets_to_opening = data.get('total_assets_to_opening')
        total_assets_to_opening = total_assets * total_assets_to_opening
        # 平均总资产
        average_total_assets = (total_assets + total_assets_to_opening) / 2
        # 净利润
        net_profit_cut = data.get('net_profit_cut')
        # 资产净利率
        self.key_dict['资产净利率'] = round(net_profit_cut / average_total_assets, 2)
        self.key_dict['销售净利润'] = data.get('net_profit_cut')
        self.key_dict['销售毛利率'] = data.get('operating_profit')

        net_profit_cut1 = self.key_dict['销售净利润']
        net_profit_cut2 = self.key_dict['销售净利润'] * data.get('ne_t_minority_ty_yoy')

        operating_profit1 = self.key_dict['销售毛利率']
        operating_profit2 = self.key_dict['销售毛利率'] * data.get('operating_profit_yoy')

        # 盈利情况判断
        if _BasicAnalysis.percent_compare(net_profit_cut1, net_profit_cut2) > 0:
            if _BasicAnalysis.percent_compare(operating_profit1, operating_profit2) > 0:
                conclusion = "毛利润和净利润显著增长"
            elif _BasicAnalysis.percent_compare(operating_profit1, operating_profit2) < 0:
                conclusion = "净利润显著增长"
            else:
                conclusion = "净利润显著增长"
        elif _BasicAnalysis.percent_compare(net_profit_cut1, net_profit_cut2) == 0:
            if _BasicAnalysis.percent_compare(operating_profit1, operating_profit2) > 0:
                conclusion = "毛利润显著增长，净利润保持稳定"
            elif _BasicAnalysis.percent_compare(operating_profit1, operating_profit2) < 0:
                conclusion = "毛利润下降，净利润保持稳定"
            else:
                conclusion = "盈利能力保持稳定"
        else:
            if _BasicAnalysis.percent_compare(operating_profit1, operating_profit2) > 0:
                conclusion = "毛利润增长但净利润下降"
            elif _BasicAnalysis.percent_compare(operating_profit1, operating_profit2) < 0:
                conclusion = "毛利和净利润双双承压"
            else:
                conclusion = "毛利润增长但净利率降低"
        self.key_dict['公司盈利情况判断'] = conclusion

    def fill_finance_performance(self, order_book_id, end_date):
        """
        填充业绩公告
        """
        data = self.service.current_performance(order_book_id, end_date)
        self.key_dict['营业收入'] = data.get("operating_revenue")
        self.key_dict['营业收入同比增长'] = data.get('operating_revenue_yoy')
        self.key_dict['净利润'] = data.get('net_profit_cut')
        self.key_dict['净利润同比增长'] = data.get('ne_t_minority_ty_yoy')

        operating_revenue1 = self.key_dict['营业收入']
        operating_revenue2 = self.key_dict['营业收入'] * self.key_dict['营业收入同比增长']

        net_profit_cut1 = self.key_dict['净利润']
        net_profit_cut2 = self.key_dict['净利润'] * self.key_dict['净利润同比增长']

        if _BasicAnalysis.percent_compare(operating_revenue1, operating_revenue2) > 0:
            if _BasicAnalysis.percent_compare(net_profit_cut1, net_profit_cut2) > 0:
                conclusion = "收入和利润稳步增长"
            elif _BasicAnalysis.percent_compare(net_profit_cut1, net_profit_cut2) < 0:
                conclusion = "收入增长，盈利能力不足"
            else:
                conclusion = "收入增长，盈利能力不足"
        elif _BasicAnalysis.percent_compare(operating_revenue1, operating_revenue2) == 0:
            if _BasicAnalysis.percent_compare(net_profit_cut1, net_profit_cut2) > 0:
                conclusion = "收入保持稳定，盈利能力显著增长"
            elif _BasicAnalysis.percent_compare(net_profit_cut1, net_profit_cut2) < 0:
                conclusion = "收入保持稳定，盈利能力不足"
            else:
                conclusion = "收入和盈利保持稳定"
        else:
            if _BasicAnalysis.percent_compare(net_profit_cut1, net_profit_cut2) > 0:
                conclusion = "收入承压但利润有所提升"
            elif _BasicAnalysis.percent_compare(net_profit_cut1, net_profit_cut2) < 0:
                conclusion = "收入与利润双双承压"
            else:
                conclusion = "收入承压但利润有所提升"
        self.key_dict['经营情况整体判断'] = conclusion

    def fill_kline_chart(self, order_book_id, start_date, end_date):
        """
        填充K线图
        """
        df = self.service.get_price(order_book_id, start_date, end_date)
        image, content_type = charts.draw_kline_chart(df, date='date', open='open', high='high', low='low',
                                                      close='close',
                                                      volume='volume')
        # 将图片留存入oss中
        uid = utils.gen_uid()
        today = pydatetime.today()
        object_name = f"{today.year}/{today.month}/{today.day}/kline-{uid}.png"
        io.upload_file(image, object_name)
        url = io.generate_path(object_name)
        self.key_dict["K线图url链接"] = url

    def fill_instrument_info(self, order_book_id):
        """
        填充标的的信息
        """
        instrument_info = self.service.get_instruments(keywords=order_book_id)
        if len(instrument_info) > 0:
            instrument_info = instrument_info[0]
        else:
            raise Exception(f"未找到【{order_book_id}】对应的股票信息")
        self.key_dict["股票名称"] = instrument_info.get("symbol")
        self.key_dict["所属行业"] = instrument_info.get("industry_name")

    @staticmethod
    def get_name():
        return "基本面分析"
