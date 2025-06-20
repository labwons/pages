from numpy import isnan, nan
from pandas import isna
from typing import Union


def krw2currency(krw: int) -> Union[str, float]:
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
        return f'{int(krw // 10000)}억 {int(krw % 10000)}만'
    return f'{int(krw // 10000)}만'

