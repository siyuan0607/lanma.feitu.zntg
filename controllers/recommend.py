import random
import analysis
from sessions import UserSessions
from controllers.resource import RestfulResource


class Recommend(RestfulResource):
    def post(self):
        user_info = self.args('user_info')
        self.sessions = UserSessions(user_info)
        entities = self.sessions.get('entities')
        if not entities: return {'code': 400, 'data': None, 'msg': '没有找到上文的分析方法'}, 400
        methods = entities['分析方法']
        instruments = entities.get('投资标的', [])
        exclusive_methods = []
        for method in methods:
            exclusive_methods.append(method)

        result = []
        full_methods = analysis.get_all_methods_dict()
        for name in full_methods.keys():
            if name in exclusive_methods: continue
            value = analysis.gen_recommend_item(name=name, instruments=instruments)
            result.append(*value)

        if len(result) > 3:
            random.shuffle(result)
            result = result[:3]
        return {'code': 200, 'data': result, 'msg': ''}, 200
