import json
import analysis
from controllers.resource import RestfulResource


class Analysis(RestfulResource):
    def post(self):
        data = self.args('data')
        result = []
        for method in data.get("methods", []):
            content = analysis.execute(method, data=data)
            result.append(content)
        result = "\n".join(result)
        return {'code': 200, 'data': result, 'msg': "success"}, 200


"""
{
            "order_book_id": "",  # 标的编号
           "symbol": "",  # 标的简称
           "title": "",  # 正文标题
           "display_content": "", # 展示名称
            "methods":[] # 分析方法标记，示例：基本面分析、财务面分析
}
"""
