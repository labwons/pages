try:
    from .bubble.generic import Basis
    from .treemap.generic import MarketMap
except ImportError:
    from dev.task.bubble.generic import Basis
    from dev.task.treemap.generic import MarketMap

basis = Basis()
basis.dump()

marketMap = MarketMap(basis)
marketMap.dump()
