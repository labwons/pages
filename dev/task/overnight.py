try:
    from ..common.logger import Log
    from ..module.wise.generic import Groups, Indices
except ImportError:
    from dev.common.logger import Log
    from dev.module.wise.generic import Groups, Indices

runGroup = Groups(offline=False).dump()
runIndex = Indices(offline=False).dump()
Log.send()