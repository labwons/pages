try:
    from ..common.logger import Log
    from ..module.wise.generic import Groups, Indices
    from ..module.ecos.generic import Ecos
except ImportError:
    from dev.common.logger import Log
    from dev.module.wise.generic import Groups, Indices
    from dev.module.ecos.generic import Ecos

Log.set_title(f"[LW][LOG] UPDATE WISE/INDEX @{Calendar}")
runGroup = Groups(offline=False).dump()
runIndex = Indices(offline=False).dump()
Ecos.dump()
Log.send()