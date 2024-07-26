class memorize(property):
    def __get__(self, *args, **kwargs):
        if not hasattr(args[0], "__mem__"):
            setattr(args[0], "__mem__", {})
        mem = getattr(args[0], "__mem__")

        key = f"_{self.fget.__name__}_"
        if not key in mem:
            mem[key] = super().__get__(*args, **kwargs)
        return mem[key]