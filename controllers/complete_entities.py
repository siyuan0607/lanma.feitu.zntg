import services
from datetime import datetime as pydatetime
from sessions import UserSessions
from controllers.resource import RestfulResource
import analysis


class CompleteEntities(RestfulResource):
    def post(self):
        """
        处理实体识别，以及基于记忆对象的实体补全
        """
        user_info = self.args('user_info')
        new_entities = self.args('key_vars')
        self.sessions = UserSessions(user_info)
        # 获取上一轮对话的实体
        entities = self.sessions.get('entities')
        # 将两个实体合并成一个，其中如果有重复的实体，将新的实体覆盖旧的实体
        if not entities:
            entities = new_entities
        else:
            entities = {**entities, **new_entities}
        code, message, entities = self.fill_instrument(entities)

        # 更新会话的实体对象
        self.sessions.set('entities', entities)
        if code >= 300:
            return {'code': code, 'data': entities, 'msg': message}, code

        code, message, entities = self.fill_methods(entities)
        if code >= 300:
            return {'code': code, 'data': entities, 'msg': message}, code

        # 更新会话的实体对象
        self.sessions.set('entities', entities)
        return {'code': code, 'msg': message, 'data': entities}, code

    def fill_instrument(self, entities):
        """
        检查其中的book_order_id，并将其转化为标准的stock_id
        """
        instruments = entities.get('投资标的', [])
        if len(instruments) == 0:
            return 401, '', {}
        service = services.DataService()
        instruments = service.get_instruments(keywords=instruments)
        # 检查filter_instruments是否有数据
        if len(instruments) == 0:
            return 400, '小凸在A股中找不到您关注的股票，请确认股票信息是否正确', {}

        entities['投资标的'] = instruments
        # 如果instruments中有value包含none，则返回201的代码，并提示某只股票没有找到
        not_found_count = 0
        not_found_instruments = []
        for key, value in instruments.items():
            if value is None:
                not_found_count += 1
                not_found_instruments.append(key)

        if 0 < not_found_count < len(instruments):
            # 返回剔除value是None的字典对象
            entities['投资标的'] = {key: value for key, value in instruments.items() if value is not None}
            return 201, f'小凸在A股中找不到您关注的股票：{", ".join(not_found_instruments)}', entities
        elif not_found_count == len(instruments):
            return 400, '小凸在A股中找不到您关注的股票，请确认股票信息是否正确', {}
        else:
            return 200, 'success', entities

    def fill_methods(self, entities):
        """
        填充分析方法
        :param entities
        """
        methods = entities.get('分析方法', [])
        if len(methods) == 0:
            return 401, '', {}

        incorrect_methods = [item for item in methods if not analysis.has_method(item)]
        if len(incorrect_methods) == len(methods):
            incorrect_methods = "、".join(incorrect_methods)
            correct_name = "、".join(analysis.get_methods_name())
            return 401, f'抱歉，您输入的“{incorrect_methods}”分析方法暂时不支持，小凸目前支持有：{correct_name}哦~', {}
        else:
            incorrect_methods = "、".join(incorrect_methods)
            if len(incorrect_methods) > 0:
                message = f'抱歉，您要求的“{incorrect_methods}”分析方法暂时不支持'
                code = 201
            else:
                message = 'success'
                code = 200
            # 将 incorrect_methods 从 methods 中剔除
            methods = [method for method in methods if method not in incorrect_methods]
            entities['分析方法'] = methods
            return code, message, entities
