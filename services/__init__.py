import config

if config.DEBUG:
    from services.mock_service import MockService as DataService
else:
    from services.prod_service import ProdService as DataService
