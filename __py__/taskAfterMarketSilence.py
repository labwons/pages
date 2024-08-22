try:
    from .sector.generic import Wise
except ImportError:
    from __py__.sector.generic import Wise


if __name__ == "__main__":
    Wise('WI26', auto_update=True)
