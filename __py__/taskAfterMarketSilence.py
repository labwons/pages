try:
    from .sector.generic import Sector
except ImportError:
    from __py__.sector.generic import Sector


if __name__ == "__main__":
    Sector(auto_update=True)
