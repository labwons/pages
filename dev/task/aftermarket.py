try:
    from .bubble.generic import Basis
    from .treemap.generic import MarketMap
    from .rank.generic import Rank
except ImportError:
    from dev.task.bubble.generic import Basis
    from dev.task.treemap.generic import MarketMap
    from dev.task.rank.generic import Rank

basis = Basis(offline=False)
basis.dump()

marketMap = MarketMap(basis)
marketMap.dump()

# rank = Rank(basis)
# rank.dump()
