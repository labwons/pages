try:
    from ...common.path import PATH
except ImportError:
    from dev.common.path import PATH
from pandas import DataFrame
import pandas as pd
import json


def fromEcos():
    with open(PATH.ECOS, 'r') as file:
        obj = json.load(file)
        print(obj)