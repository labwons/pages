try:
    from ..module.wise.generic import Groups, Indices
except ImportError:
    from dev.module.wise.generic import Groups, Indices

runGroup = Groups().dump()
runIndex = Indices().dump()