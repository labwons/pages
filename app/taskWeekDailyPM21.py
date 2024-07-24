try:
    from .common import path
    from .sector.generic import wise
    from .sector import core
except ImportError:
    from app.common import path
    from app.sector.generic import wise
    from app.sector import core

wise(core.WI26).set_index(keys='ticker').to_json(path.JSONWI26, orient='index')