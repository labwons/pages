try:
    from ._ecos import Ecos
    from ._fred import Fred
except ImportError:
    from src.fetch.macro._ecos import Ecos
    from src.fetch.macro._fred import Fred



class Macro:

    def __init__(self):
        return