import numpy as np

def str2num(src:str) -> int or float:
    if not src:
        return np.nan
    try:
        return float(src) if "." in src else int(src)
    except ValueError:
        src = "".join([c for c in src if c.isdigit() or c in [".", "-"]])
        if not src or src == "." or src == "-":
            return None
        if "." in src:
            return float(src)
        return int(src)