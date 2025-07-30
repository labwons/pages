from numpy import nan, isnan
from pandas import Series, isna
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from typing import Dict, List, Union
import csscompressor, rjsmin, os, shutil


class eMail(MIMEMultipart):

    _context:str = ''

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
    def context(self) -> str:
        return self._context

    @context.setter
    def context(self, context:str):
        self._context = context

    def send(self):
        self.attach(MIMEText(self.context))
        with SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(self.sender, "puiz yxql tnoe ivaa")
            server.send_message(self)
        return


def navigate(root:str) -> List[Dict[str, Union[str, dict]]]:
    CONTENT_NAMES = {
        "bubble": "종목 발굴",
        "macro": "경제 지표",
    }
    nav: List[Dict] = [{"href": f"/", "content": "시장 지도"}]
    for content in CONTENT_NAMES:
        if not content in os.listdir(root):
            continue
        nav.append({'href': f'/{content}', 'content': CONTENT_NAMES[content]})
        if content == "portfolio":

            sub = []
            for sub_content in os.listdir(os.path.join(root, content)):
                if sub_content.startswith('index'):
                    continue
                name = ""
                sub.append({'href': f'/{content}/{sub_content}', 'content': name})
            nav[-1].update({'sub': sub})
    return nav


def minify(root:str):
    for _dir, _folder, _files in os.walk(root):
        for _file in _files:
            if _file.endswith('js') and not _file.endswith('.min.js'):
                js = os.path.join(_dir, _file)
                with open(js, 'r', encoding='utf-8') as file:
                    src = file.read()
                with open(js.replace(".js", ".min.js"), "w", encoding='utf-8') as file:
                    file.write(rjsmin.jsmin(src))
            elif _file.endswith('css') and not _file.endswith('.min.css'):
                css = os.path.join(_dir, _file)
                with open(css, 'r', encoding='utf-8') as file:
                    src = file.read()
                with open(css.replace(".css", ".min.css"), "w", encoding='utf-8') as file:
                    file.write(csscompressor.compress(src))
            else:
                continue
    return

def typeCast(value):
    value = str(value).lower().replace(",", "")
    if value in ['separate', 'consolidated']:
        return value
    if "n" in value:
        return nan
    if not any([char.isdigit() for char in value]):
        return nan
    return float(value) if "." in value or "-" in value else int(value)


def profitGrowth(profit:Series, debug:bool=False) -> List:
    prev = profit.values[0]
    if -1 <= prev <= 1:
        prev = nan
    value, label = [], []
    for curr in profit.iloc[1:]:
        if -1 <= curr <= 1:
            curr = nan
        if prev is None or isna(prev) or isna(curr) or isnan(prev) or isnan(curr):
            value.append(nan)
            label.append(nan)
        elif prev < 0 <= curr:
            value.append(nan)
            label.append("흑자 전환")
        elif curr < 0 <= prev:
            value.append(nan)
            label.append("적자 전환")
        else:
            value.append(100 * (curr - prev) / abs(prev))
            label.append(nan)
        prev = curr
    values = Series(value)
    average = values.mean() if len(values.dropna()) >= 2 else nan
    if debug:
        print(values)
        print(average)
    return [value[-1], label[-1], average]

def clearPath(path:str):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            pass
