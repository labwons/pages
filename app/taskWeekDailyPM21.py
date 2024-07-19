try:
    from .sector.wise import wise
    from .sector.core.key import WICS, WI26
except ImportError:
    from app.sector.wise import wise
    from app.sector.core.key import WICS, WI26
import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))
DISTDIR = os.path.join(BASEDIR, '..', 'map')
WICSDIR = os.path.join(DISTDIR, r"src/json")
WI26DIR = os.path.join(DISTDIR, r"src/json")
if not os.path.isdir(WICSDIR):
    os.makedirs(WICSDIR)
if not os.path.isdir(WI26DIR):
    os.makedirs(WI26DIR)

wics = wise(WICS)
wi26 = wise(WI26)
wics.to_json(os.path.join(WICSDIR,"wics.json"), orient='index')
wi26.to_json(os.path.join(WICSDIR,"wi26.json"), orient='index')