try:
    from .common import path
    from .sector.wise import wise
    from .sector.core import key
except ImportError:
    from app.common import path
    from app.sector.wise import wise
    from app.sector.core import key

wise(key.WICS).set_index(keys='ticker').to_json(path.JSONWICS, orient='index')
# Deprecated WI26
# wise(key.WI26).set_index(keys='ticker').to_json(path.JSONWI26, orient='index')