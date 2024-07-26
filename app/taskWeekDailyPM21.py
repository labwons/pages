try:
    from .common import PATH
    from .sector.generic import Wise
    from .sector.fetch import KEY
except ImportError:
    from app.common import PATH
    from app.sector.generic import Wise
    from app.sector.fetch import KEY

if __name__ == "__main__":
    Wise("WI26") \
    .to_json(
        path_or_buf=PATH.JSONWI26, 
        orient='index'
    )
    
    Wise("WICS") \
    .to_json(
        path_or_buf=PATH.JSONWICS, 
        orient='index'
    )
