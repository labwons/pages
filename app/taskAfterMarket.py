try:
    # from .barmap.generic import BarMap
    from .market.generic import Market
    from .sector.generic import Wise
except ImportError:
    # from app.barmap.generic import BarMap
    from app.market.generic import Market
    from app.sector.generic import Wise


if __name__ == "__main__":
    wics = Wise('wics', auto_update=False)
    market = Market(auto_update=True)
    # print(wics.join(market, how='left'))