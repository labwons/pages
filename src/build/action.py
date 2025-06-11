try:
    from ..common.env import dDict
except ImportError:
    from src.common.env import dDict

class actionDict(dDict):
    def reset(self):
        for key in self:
            self[key] = False
        return

ACTION = actionDict(
    AFTERMARKET=True,
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
