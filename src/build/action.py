try:
    from ..common.env import Dict
except ImportError:
    from src.common.env import Dict

class actionDict(Dict):
    def reset(self):
        for key in self:
            self[key] = False
        return

ACTION = actionDict(
    AFTERMARKET=False,
    MACRO=False,
    STATEMENT=False,
    SECTOR=False
)

if __name__ == "__main__":
    print(ACTION)
    ACTION.reset()
    print(ACTION)
    ACTION.MACRO = ACTION.STATEMENT = True
    print(ACTION)
