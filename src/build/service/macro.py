try:
    from ...fetch.macro.fred import Fred
except ImportError:
    from src.fetch.macro.fred import Fred
from pandas import DataFrame, read_json
from time import time
from typing import List
if "PATH" not in globals():
    try:
        from ...common.path import PATH
    except ImportError:
        from src.common.path import PATH


class macro(DataFrame):

    _log: List[str] = []
    def __init__(self, update:bool=False):
        stime = time()
        self.log = f'RUN [Build Macro Cache]'
        if not update:
            super().__init__(read_json(PATH.MACRO, orient='index'))
            self.log = f'END [Build Macro Cache]'
            return

        fred = Fred()

        super().__init__(fred)
        self.log = f'END [Build Macro Cache] / Elapsed: {time() - stime:.2f}s'
        return

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    macro = macro()
    print(macro)
    print(macro.log)