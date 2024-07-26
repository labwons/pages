try:
    from .barmap.generic import BarMap
    from .sector.fetch import KEY
    from .common import PATH
except ImportError:
    from app.barmap.generic import BarMap
    from app.sector.fetch import KEY
    from app.common import PATH
    
syntax = ""
    
WICS = BarMap(KEY.WICS)
WICS.LargeCap.to_json(syntax)
WICS.LargeCap.Sector.to_json(syntax)
WICS.MidCap.to_json(syntax)

WI26 = BarMap(KEY.WI26)
WI26.LargeCap.to_json(syntax)
WI26.LargeCap.Industry.to_json(syntax)
WI26.MidCap.to_json(syntax)

with open(PATH.JSON, 'w', encoding='utf-8') as file:
    file.write(syntax)