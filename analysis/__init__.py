from analysis.basic import _BasicAnalysis as BasicAnalysis
from analysis.finance import _FinanceAnalysis as FinanceAnalysis
from analysis.public_opinion import _PublicOpinionAnalysis as PublicOpinionAnalysis
from analysis.stock_quotes import _StockQuotesAnalysis as StockQuotesAnalysis
from analysis.trade import _TradeAnalysis as TradeAnalysis

methods = None
_init = False


def _initialize():
    global methods
    global _init
    methods = {BasicAnalysis.get_name(): BasicAnalysis, FinanceAnalysis.get_name(): FinanceAnalysis,
               PublicOpinionAnalysis.get_name(): PublicOpinionAnalysis,
               StockQuotesAnalysis.get_name(): StockQuotesAnalysis, TradeAnalysis.get_name(): TradeAnalysis}
    _init = True


def get_all_methods_dict():
    global methods
    global _init
    if not _init:
        _initialize()
    return methods


def get_methods_name():
    global methods
    global _init
    if not _init:
        _initialize()
    return list(methods.keys())


def has_method(name: str):
    global methods
    global _init
    if not _init:
        _initialize()
    return name in methods


def execute(name: str, **kwargs):
    global methods
    global _init
    if not _init:
        _initialize()
    if name not in methods:
        raise Exception(f"analysis method: {name} not found")
    instance = methods.get(name)()
    return instance.execute(**kwargs)


def gen_recommend_item(name: str, **kwargs):
    global methods
    global _init
    if not _init:
        _initialize()
    if name not in methods:
        raise Exception(f"analysis method: {name} not found")
    instruments = kwargs.get('instruments', [])
    result = []
    for key, value in instruments.items():
        order_book_id = value.get('order_book_id')
        symbol = value.get('symbol')
        result.append({
            'order_book_id': order_book_id,
            'symbol': symbol,
            'methods': [name],
            'display_content': f'查看{symbol}({order_book_id}) 的{name}'
        })
    return result