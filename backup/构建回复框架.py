import json


def build_response(data):
    msg = data.get('msg')
    code = data.get('code')
    data = data.get('data')
    warning = ''
    if len(msg) > 0:
        warning = msg
    result = {
        'warning': warning,
        'reply': [],
        'recommend': 1
    }
    for key, instrument in data['投资标的'].items():
        symbol = instrument['symbol']
        order_book_id = instrument['order_book_id']
        result['reply'].append({
            'order_book_id': instrument['order_book_id'],
            'symbol': instrument['symbol'],
            'title': f'{symbol} ({order_book_id})的分析',
            'display_content': '',
            'methods': data['分析方法']

        })
    result = json.dumps(result)
    return result


def main():
    data = 关键变量
    data = json.dumps(data)
    最终回复 = build_response(data)


main()