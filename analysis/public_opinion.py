from analysis.base import _BaseAnalysis
import services
import json


class _PublicOpinionAnalysis(_BaseAnalysis):
    def __init__(self) -> None:
        self.service = services.DataService()
        super().__init__()

    def execute(self, **kwargs):
        order_book_id = kwargs.get('order_book_id')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        instrument_info = self.service.get_instruments(keywords=order_book_id)
        symbol = instrument_info.get('symbol')
        df = self.service.get_stock_news(order_book_id=order_book_id, start_date=start_date, end_date=end_date)
        data = df.to_json()
        data = json.loads(data)
        result = {
            'msg': f'{symbol}最近的舆情，以行业发展相关舆情为主，详细的舆情情况见下：',
            'list': []
        }
        length = len(data) if len(data) < 5 else 5
        for i in range(length):
            result['list'].append({
                'title': data[i]['title'],
                'original_time': data[i]['original_time'],
                'source': data[i]['source'],
                'news_emotion_indicator': data[i]['news_emotion_indicator'],
                'url': data[i]['url']
            })
        result = json.dumps(result)
        result = "-list-\n" + result
        return result

    @staticmethod
    def get_name():
        return '舆情分析'
