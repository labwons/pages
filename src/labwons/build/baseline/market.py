from labwons.logs import build_logger as logger
from labwons.path import ARCHIVE
from labwons.build.schema import FIELD

from datetime import datetime
from pandas import DataFrame, Series
from time import perf_counter
import numpy as np
import pandas as pd


class BaselineMarket:

    def __init__(self):
        stime = perf_counter()
        self.status = "FAILED"

        # logger.info(f'RUN [BUILD MARKET BASELINE]')



if __name__ == "__main__":
    baseline = BaselineMarket()
