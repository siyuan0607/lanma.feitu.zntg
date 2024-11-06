import config
from utils import get_logger
from flask import Flask
from flask_restful import Api
import rqdatac

from controllers.complete_entities import CompleteEntities
from controllers.analysis import Analysis
from controllers.recommend import Recommend

logger = get_logger(__name__)
app = Flask(__name__)
api = Api(app)

# rests的路由服务
api.add_resource(CompleteEntities, '/rests/complete_entities')
api.add_resource(Analysis, '/rests/analysis')
api.add_resource(Recommend, '/rests/recommend')

# 初始化rqdatac
# rqdatac.init('license', 'GP4UL1nwUmS_s-k2RG5bAtdzv1z9XNsZKW5XUEkES91AQBSK0eN2OXvmZXX7KnF6eJH-VE-vnPRe5B61GgX5ou0tGZoT_IMzqN_s2PUU_r7p7Mj88kfbolM37-dk-A6w00BYpDlkD4fszJqECm5_YX6QoWSSsCL4oN1V8piByaI=QL_dZ2P6-cnWCrXe82oiufaUthylqEkfk...: z5EFka4UAQ85SlPzi5zVl_G02MXKP8fp9ni19Ltau4lsHkNb05d7IHetwxUIEfeNa1hxIK-JISqRM2xnraP2RMt-ti7xNfUKCSbe7w-1vA2vGnPFZAfzk-jm1OgYXx_CCJPC9Kf5OA=')

logger.info(f"server start at port {config.PORT}")
app.run(port=config.PORT)
logger.info("server stop")
