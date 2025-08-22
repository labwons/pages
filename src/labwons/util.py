from labwons.deco import classproperty
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pykrx.stock import get_nearest_business_day_in_a_week
from smtplib import SMTP
from time import sleep
import pprint


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
    def TIME(cls) -> str:
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
                setattr(cls, '__td__', None)
        return getattr(cls, '__td__')



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


# Alias
dD = DD = dDict = DataDictionary

if __name__ == "__main__":
    print(DATETIME.TRADING)