from labwons.deco import classproperty

from bs4 import BeautifulSoup
from datetime import datetime, time, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from json import JSONDecoder
from pandas import DataFrame
from pykrx.stock import get_nearest_business_day_in_a_week
from smtplib import SMTP
from time import sleep
from typing import Dict, Union
from urllib.request import urlopen

import numpy as np
import pandas as pd
import pprint, warnings, json, re, requests
warnings.filterwarnings("ignore")


class DATETIME:

    @classmethod
    def pause(cls, sec:int):
        sleep(sec)
        return

    @classmethod
    def CLOCK(cls) -> datetime:
        return datetime.now(timezone(timedelta(hours=9)))
    
    @classmethod
    def DATE(cls):
        return cls.CLOCK().date()

    @classmethod
    def TIME(cls) -> time:
        return cls.CLOCK().time()
    
    @classproperty
    def TODAY(cls) -> str:
        return cls.CLOCK().strftime("%Y%m%d")
    
    @classproperty
    def TRADING(cls) -> str:
        if not hasattr(cls, '__td__'):
            try:
                setattr(cls, '__td__', get_nearest_business_day_in_a_week())
            except (IndexError, Exception):
                return None
        return getattr(cls, '__td__')

    @classproperty
    def WISE(cls) -> str:
        if not hasattr(cls, '__wi__'):
            try:
                date = re.compile(r"var\s+dt\s*=\s*'(\d{8})'") \
                    .search(requests.get('https://www.wiseindex.com/Index/Index#/G1010.0.Components').text) \
                    .group(1)
                setattr(cls, '__wi__', date)
            except (IndexError, Exception):
                return None
        return getattr(cls, '__wi__')


class Mail(MIMEMultipart):

    _content:str = ''

    def __init__(self):
        super().__init__()
        self['From'] = 'snob.labwons@gmail.com'
        self['To'] = 'jhlee_0319@naver.com'
        return

    @property
    def subject(self) -> str:
        return self['Subject']

    @subject.setter
    def subject(self, subject:str):
        self['Subject'] = subject

    @property
    def sender(self):
        return self['From']

    @sender.setter
    def sender(self, sender:str):
        self['From'] = sender

    @property
    def receiver(self):
        return self['To']

    @receiver.setter
    def receiver(self, receiver:str):
        self['To'] = receiver

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, content:str):
        self._content = content

    def send(self):
        self.attach(MIMEText(self.content))
        with SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(self.sender, "puiz yxql tnoe ivaa")
            server.send_message(self)
        return


class DataDictionary(dict):
    """
    데이터 저장 Dictionary
    built-in: dict의 확장으로 저장 요소에 대해 attribute 접근 방식을 허용
    기본 제공 Alias (별칭): dD, dDict

    사용 예시)
        myData = DataDictionary(name='JEHYEUK', age=34, division='Vehicle Solution Team')
        print(myData.name, myData['name'], myData.name == myData['name'])

        /* ----------------------------------------------------------------------------------------
        | 결과
        -------------------------------------------------------------------------------------------
        | JEHYEUK JEHYEUK True
        ---------------------------------------------------------------------------------------- */
    """
    def __init__(self, data=None, **kwargs):
        super().__init__()

        data = data or {}
        data.update(kwargs)
        for key, value in data.items():
            if isinstance(value, dict):
                value = DataDictionary(**value)
            self[key] = value

    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        return super().__getattribute__(attr)

    def __setattr__(self, attr, value):
        if isinstance(value, dict):
            self[attr] = DataDictionary(**value)
        else:
            self[attr] = value

    def __str__(self) -> str:
        return pprint.pformat(self)


class DataProcessing:

    @classmethod
    def krw2currency(cls, krw: int) -> Union[str, float]:
        """
        KRW (원화) 입력 시 화폐 표기 법으로 변환(자동 계산)
        @krw 단위는 원 일 것
        """
        if pd.isna(krw) or np.isnan(krw):
            return np.nan
        if krw >= 1e+12:
            krw /= 1e+8
            currency = f'{int(krw // 10000)}조'
            if int(krw % 10000):
                currency += f' {int(krw % 10000)}억'
            return currency

        if krw >= 1e+10:
            krw /= 1e+4
            currency = f'{int(krw // 10000)}억'
            return currency

        if krw >= 1e+8:
            krw /= 1e+4
            currency = f'{int(krw // 10000)}억'
            if int(krw % 10000):
                currency += f' {int(krw % 10000)}만'
            return currency
        return f'{int(krw // 10000)}만'

    @classmethod
    def str2num(cls, src: str) -> int or float:
        if isinstance(src, float):
            return src
        if src is None:
            return np.nan
        src = "".join([char for char in src if char.isdigit() or char == "."])
        if not src or src == ".":
            return np.nan
        if "." in src:
            return float(src)
        return int(src)

    @classmethod
    def deleteKeysFromString(cls, string:str, *keys) -> str:
        for key in keys:
            string = string.replace(key, '')
        return string

    @classmethod
    def delKeys(cls, string:str, *keys) -> str:
        return cls.deleteKeysFromString(string=string, *keys)



class multiframes(DataFrame):

    __mem__ = {}
    def __init__(self, frames:Dict[str, DataFrame]):
        base = list(frames.values())[0]
        self.__mem__ = frames.copy()
        super().__init__(data=base.values, index=base.index, columns=base.columns)
        return

    def __getattr__(self, item):
        if item in self.__mem__:
            return self.__mem__[item]
        return super().__getattr__(name=item)


class _web(object):

    def req(self, url:str):
        attr = f"_req_{url}_"
        if not hasattr(self, attr):
            req = requests.get(url, verify=False)
            if not req.status_code == 200:
                raise ConnectionError
            self.__setattr__(attr, req)
        return self.__getattribute__(attr)

    def html(self, url:str, parser:str="") -> BeautifulSoup:
        attr = f"_html_{url}_"
        if not hasattr(self, attr):
            parser = parser if parser else 'xml' if url.endswith('.xml') else 'lxml'
            self.__setattr__(attr, BeautifulSoup(self.req(url).text, parser))
        return self.__getattribute__(attr)

    def list(self, url:str, encoding:str='utf-8', displayed_only:bool=False) -> list:
        attr = f"_list_{url}_"
        if not hasattr(self, attr):
            encoding = "euc-kr" if "naver" in url else encoding
            self.__setattr__(attr, pd.read_html(io=url, header=0, encoding=encoding, displayed_only=displayed_only))
        return self.__getattribute__(attr)

    def json(self, url:str) -> JSONDecoder:
        attr = f"_json_{url}_"
        if not hasattr(self, attr):
            data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace').replace(" ", "").replace("\t", ""))
            self.__setattr__(attr, data)
        return self.__getattribute__(attr)

    def data(self, url:str, key:str=""):
        if url.endswith('.json'):
            return DataFrame(self.json(url)[key] if key else self.json(url))
        elif url.endswith('.csv'):
            return pd.read_csv(url, encoding='utf-8')
        elif url.endswith('.pkl'):
            return pd.read_pickle(url)
        else:
            raise KeyError(f"Unknown data type: {url}")

# Alias
dD = DD = dDict = DataDictionary
dP = DP = dProc = DataProcessing
web = _web()


if __name__ == "__main__":
    # print(DP.krw2currency(21234659857382)) # 21조 2346억
    # print(DP.krw2currency( 1234659857382)) #  1조 2346억
    print(DP.krw2currency(  234659857382)) #      2346억
    print(DP.krw2currency(   34659857382)) #       346억
    print(DP.krw2currency(    4659857382)) #
    print(DP.krw2currency(     659857382)) #
    print(DP.krw2currency(      59857382)) #
    print(DP.krw2currency(       9857382)) #
    print(DP.krw2currency(        857382)) #