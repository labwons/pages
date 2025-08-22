import pprint


class metaClass(type):
    """
    클래스 자체의 던더 메소드 정의를 위한 메타 클래스
    메타 클래스로 지정할 경우 하위 클래스 변수를 명시적으로 지정해주어야 함.
    """
    __iterable__ = None
    __string__ = None

    def __iter__(cls) -> iter:
        if cls.__iterable__ is None:
            raise TypeError('Not Iterable: {cls.__iterable__} is not defined')
        return iter(cls.__iterable__)

    def __str__(cls) -> str:
        if cls.__string__ is None:
            raise TypeError('Not Printable: {cls.__string__} is not defined')
        return str(cls.__string__)


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

    def __iter__(self):
        for key, value in self.items():
            yield key, value

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
dD = dDict = DataDictionary