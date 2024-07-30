try:
    from .sector.generic import Wise
except ImportError:
    from app.sector.generic import Wise


if __name__ == "__main__":
    Wise('WICS', auto_update=True)
    Wise('WI26', auto_update=True)
