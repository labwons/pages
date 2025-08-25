from labwons.logs import fetch_logger as logger
from pandas import concat, DataFrame, read_json, read_parquet, Series
from re import DOTALL, sub
from requests import get
from time import perf_counter
from typing import Any, List, Union
from xml.etree.ElementTree import Element, fromstring


class FinancialStatement:

    def __init__(self, *tickers):
        if not len(tickers):
            self.status = "PASSED"
            logger.info(f"{self.status} [FETCH FNGUIDE DATA]")
            return

        stime = perf_counter()
        self.status = "FAILED"
        logger.info(f"RUN [FETCH FNGUIDE DATA]")

        overview, annual, quarter = [], {}, {}
        for ticker in tickers:
            xml = self.fetch(ticker, debug=False)
            if xml is None:
                logger.warn(f"- EMPTY XML FOR TICKER: {ticker}")
                self.status = "INCOMPLETE"
                continue

            numbers = self.numbers(xml, name=ticker)
            bd = self.statementType(xml)
            # EXCEPTION FOR STATEMENT TYPE
            if ticker in ['021320']:
                bd = "separate"

            annual[ticker] = a = self.statement(xml, bd, 'annual')
            quarter[ticker] = q = self.statement(xml, bd, 'quarter')

            numbers['statementType'] = bd
            numbers['reportYears'] = ','.join([i for i in a.index])
            numbers['reportQuarters'] = ','.join([i for i in q.index])
            overview.append(numbers)

        self.overview = concat(overview, axis=1).T
        self.annual = concat(annual, axis=1)
        self.quarter = concat(quarter, axis=1)
        date = self.overview['date'].value_counts(dropna=False)
        if len(date) == 1:
            logger.info(f'- RESOURCE DATE: {date.index[0]}')
        else:
            report = '/'.join(f'{line}' for line in str(date).split('\n')[1:-1])
            logger.warn(f'- RESOURCE DATE: LOW RELIABILITY :: {report}')
        logger.info(f'END [FETCH FNGUIDE DATA] {len(tickers):,d} ITEMS: {perf_counter() - stime:.2f}s')

        if self.status == "FAILED":
            self.status = "OK"
        return

    def fetchOverview(self, path:str):
        if self.status == "OK":
            self.overview.to_parquet(path, engine='pyarrow')
        return

    def fetchAnnualStatement(self, path:str):
        if self.status == "OK":
            self.annual.to_parquet(path, engine='pyarrow')
        return

    def fetchQuarterStatement(self, path:str):
        if self.status == "OK":
            self.quarter.to_parquet(path, engine='pyarrow')
        return

    @classmethod
    def _statement(cls, xml: Element, tag: str) -> DataFrame:
        # TO MINIMIZE MEMORY USAGE, SOME COLUMN KEYS ARE TO BE DROPPED.
        EXCLUDE = [
            '영업이익(발표기준)', '자본금(억원)',
            '지배주주순이익(억원)', '비지배주주순이익(억원)', '순이익률(%)',
            '지배주주지분(억원)', '비지배주주지분(억원)', '지배주주순이익률(%)',
            '발행주식수(천주)',
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
            logger.error(f'- FAILED TO FETCH TICKER: {ticker} / {reason}')
        return

    @classmethod
    def numbers(cls, ticker_or_xml: Union[str, Element], name: str = None) -> Series:
        xml = cls.fetch(ticker_or_xml) if isinstance(ticker_or_xml, str) else ticker_or_xml
        obj = {child.tag: child.text for child in xml.find('price')}
        if xml.find('consensus') is not None:
            obj.update({child.tag: child.text for child in xml.find('consensus')})
        return Series(obj, name=name)

    @classmethod
    def statementType(cls, xml:Element) -> str:
        sy = cls._statement(xml, 'financial_highlight_ifrs_B/financial_highlight_annual')
        cy = cls._statement(xml, 'financial_highlight_ifrs_D/financial_highlight_annual')
        sq = cls._statement(xml, 'financial_highlight_ifrs_B/financial_highlight_quarter')
        cq = cls._statement(xml, 'financial_highlight_ifrs_D/financial_highlight_quarter')
        if (sy.count().sum() > cy.count().sum()) or (sq.count().sum() > cq.count().sum()):
            return 'separate'
        else:
            return 'consolidated'

    @classmethod
    def statement(cls, ticker_or_xml: Union[str, Element], bd:str, period:str):
        xml = cls.fetch(ticker_or_xml) if isinstance(ticker_or_xml, str) else ticker_or_xml
        bd = {'separate': 'B', 'consolidated': 'D'}[bd]
        return cls._statement(xml, f'financial_highlight_ifrs_{bd}/financial_highlight_{period}')

    @classmethod
    def checkTickers(cls, baseline: str, statement: str = '') -> List[str]:
        def _read(file: str) -> DataFrame:
            if file.endswith('.json'):
                return read_json(file, orient='index')
            elif file.endswith('.parquet'):
                return read_parquet(file)

        b = _read(baseline)
        b.index = b.index.astype(str).str.zfill(6)
        if not statement:
            return b.index.tolist()

        s = _read(statement)
        s.index = s.index.astype(str).str.zfill(6)
        return [ticker for ticker in b.index if not ticker in s.index]

