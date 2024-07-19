try:
    from .sector.wise import wise
    from .sector.core.key import WICS, WI26
except ImportError:
    from app.sector.wise import wise
    from app.sector.core.key import WICS, WI26
    

wics = wise(WICS)
wi26 = wise(WI26)
wics.to_json(r"../map/src/json/wics.json", orient='index')
wi26.to_json(r"../map/src/json/wi26.json", orient='index')