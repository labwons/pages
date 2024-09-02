try:
    from .sector.generic import Sector, Index
except ImportError:
    from __py__.sector.generic import Sector, Index


if __name__ == "__main__":
    Sector(auto_update=True)
    Index()
