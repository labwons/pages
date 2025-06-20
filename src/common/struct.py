class dDict(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = dDict(**value)
            self[key] = value

    def __iter__(self):
        return iter(self.items())

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(f"No such attribute: {attr}")

    def __setattr__(self, attr, value):
        self[attr] = value
