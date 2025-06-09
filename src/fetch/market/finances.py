from pandas import (
    concat,
    DataFrame,
    read_json,
    Series
)
from re import DOTALL, sub
from requests import get
from time import time
from typing import Any, List, Union
from xml.etree.ElementTree import Element, fromstring

if not "FILE" in globals():
    try:
        from ...common.env import FILE
    except ImportError:
        from src.common.env import FILE



class FinancialStatement:
    _log: List[str] = []

    def __init__(self, update:bool=False, *tickers):
        if not update:
            return

        stime = time()
        if update and tickers:
            self.tickers = list(tickers)
            self.log = f'RUN [Build Numbers Cache] PARTIAL UPDATE N={len(tickers)}'
        else:
            self.log = f'RUN [Build Numbers Cache] FULL UPDATE'
            baseline = read_json(FILE.BASELINE, orient='index')
            baseline.index = baseline.index.astype(str).str.zfill(6)
            self.tickers = baseline.index

        overview, annual, quarter = [], {}, {}
        for ticker in self.tickers:
            xml = self.fetch(ticker, debug=False)
            if xml is None:
                self.log = f'... Empty xml or Failed to fetch: {ticker}'
                continue
            overview.append(self.numbers(xml, name=ticker))
            annual[ticker] = self.annualStatement(xml)
            quarter[ticker] = self.quarterStatement(xml)

        self.overview = concat(overview, axis=1)
        self.annual = concat(annual, axis=1)
        self.quarter = concat(quarter, axis=1)

        self.log = f'END [Build Numbers Cache] {len(self):,d} Stocks / Elapsed: {time() - stime:.2f}s'
        return

    def __len__(self):
        return len(self.tickers)

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)

    @classmethod
    def _statement(cls, xml:Element, tag: str) -> DataFrame:
        # TO MINIMIZE MEMORY USAGE, SOME COLUMN KEYS ARE TO BE DROPPED.
        EXCLUDE = [
            '영업이익(발표기준)', '자본금(억원)',
            '지배주주순이익(억원)', '비지배주주순이익(억원)', '순이익률(%)',
            '지배주주지분(억원)', '비지배주주지분(억원)', '지배주주순이익률(%)',
            'BPS(원)', 'DPS(원)', '발행주식수(천주)',
        ]
        obj = xml.find(tag)
        if obj is None:
            return DataFrame()
        columns = [val.text.replace(" ", "") for val in obj.findall('field')]
        selector = [col for col in columns if not col in EXCLUDE]
        index, data = [], []
        for record in obj.findall('record'):
            index.append(record.find('date').text)
            data.append([val.text for val in record.findall('value')])
        return DataFrame(index=index, columns=columns, data=data)[selector]

    @classmethod
    def fetch(cls, ticker: str, debug: bool = False) -> Union[Any, Element]:
        try:
            resp = get(url=f"http://cdn.fnguide.com/SVO2/xml/Snapshot_all/{ticker}.xml")
            resp.encoding = 'euc-kr'
            text = resp.text.replace("<![CDATA[", "").replace("]]>", "")
            text = sub(r'<business_summary>.*?</business_summary>', '', text, flags=DOTALL)
            if debug:
                print(text)
            return fromstring(text)
        except Exception as reason:
            cls._log.append(f'... Failed to fetch: {ticker} / {reason}')
        return

    @classmethod
    def numbers(cls, ticker_or_xml: Union[str, Element], name: str = None) -> Series:
        xml = cls.fetch(ticker_or_xml) if isinstance(ticker_or_xml, str) else ticker_or_xml
        obj = {child.tag: child.text for child in xml.find('price')}
        if xml.find('consensus') is not None:
            obj.update({child.tag: child.text for child in xml.find('consensus')})
        return Series(obj, name=name)

    @classmethod
    def annualStatement(cls, ticker_or_xml: Union[str, Element]) -> DataFrame:
        xml = cls.fetch(ticker_or_xml) if isinstance(ticker_or_xml, str) else ticker_or_xml
        separate = cls._statement(xml, 'financial_highlight_ifrs_B/financial_highlight_annual')
        consolidate = cls._statement(xml, 'financial_highlight_ifrs_D/financial_highlight_annual')
        return concat({'별도': separate, '연결': consolidate}, axis=1)

    @classmethod
    def quarterStatement(cls, ticker_or_xml: Union[str, Element]) -> DataFrame:
        xml = cls.fetch(ticker_or_xml) if isinstance(ticker_or_xml, str) else ticker_or_xml
        separate = cls._statement(xml, 'financial_highlight_ifrs_B/financial_highlight_quarter')
        consolidate = cls._statement(xml, 'financial_highlight_ifrs_D/financial_highlight_quarter')
        return concat({'별도': separate, '연결': consolidate}, axis=1)


if __name__ == "__main__":
    fs = FinancialStatement(update=False)
    print(fs.log)
