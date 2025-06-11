# PUSH TRIGGERS ACTION
# ACTION DATE: 2025.06.11. 21:00

class ACTION:

    AFTERMARKET:bool = True
    MACRO:bool       = False
    STATEMENT:bool   = False
    SECTOR:bool      = False

    @classmethod
    def reset(cls):
        for key in dir(cls):
            if not key.startswith('_'):
                setattr(cls, key, False)
        return


if __name__ == "__main__":
    print(ACTION.AFTERMARKET)
    ACTION.reset()
    print(ACTION.AFTERMARKET)
    ACTION.MACRO = ACTION.STATEMENT = True
    print(ACTION.STATEMENT)
    print(ACTION.MACRO)
