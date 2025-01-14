from pandas import DataFrame


class Trace:

    def __init__(self, data:DataFrame):
        self.data = data.copy()
        return

    def __getitem__(self, item):
        return