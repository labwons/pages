from numpy import isnan, nan
from pandas import isna
from typing import Union


def krw2currency(krw: int, limit:str='') -> Union[str, float]:
    """
    KRW (원화) 입력 시 화폐 표기 법으로 변환(자동 계산)
    @krw 단위는 원 일 것
    """
    if isna(krw) or isnan(krw):
        return nan
    if krw >= 1e+12:
        krw /= 1e+8
        return f'{int(krw // 10000)}조 {int(krw % 10000)}억'
    if krw >= 1e+8:
        krw /= 1e+4
        if limit == '억':
            return f'{int(krw // 10000)}억'
        return f'{int(krw // 10000)}억 {int(krw % 10000)}만'
    return f'{int(krw // 10000)}만'

def str2num(src: str) -> int or float:
    if isinstance(src, float):
        return src
    src = "".join([char for char in src if char.isdigit() or char == "."])
    if not src or src == ".":
        return nan
    if "." in src:
        return float(src)
    return int(src)