try:
    from .common import PATH
    from .sector.generic import wise
    from .sector.fetch import KEY
except ImportError:
    from app.common import PATH
    from app.sector.generic import wise
    from app.sector.fetch import KEY

wise(KEY.WI26) \
  .to_json(
      path_or_buf=PATH.JSONWI26, 
      orient='index'
  )
  
wise(KEY.WICS) \
  .to_json(
      path_or_buf=PATH.JSONWICS, 
      orient='index'
  )