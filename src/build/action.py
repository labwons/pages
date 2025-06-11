
class ACTION:

    AFTERMARKET=True
    MACRO=False
    STATEMENT=False
    SECTOR=False

    @classmethod
    def reset(cls):
        for key in dir(cls):
            if not key.startswith('_'):
                setattr(cls, key, False)
        return




# ACTION = actionDict(
#     AFTERMARKET=True,
#     MACRO=False,
#     STATEMENT=False,
#     SECTOR=False
# )

if __name__ == "__main__":
    print(ACTION)
    print(ACTION.AFTERMARKET)
    ACTION.reset()
    print(ACTION.AFTERMARKET)
    # print(ACTION)
    # ACTION.MACRO = ACTION.STATEMENT = True
    # print(ACTION)
    # print(ACTION.MACRO)