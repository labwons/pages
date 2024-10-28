try:
    from ..common.logger import Log
    from ..module.wise.generic import Groups, Indices
except ImportError:
    from dev.common.logger import Log
    from dev.module.wise.generic import Groups, Indices

runGroup = Groups().dump()
runIndex = Indices().dump()
Log.send()