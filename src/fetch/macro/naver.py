from bs4 import BeautifulSoup
import requests, warnings
warnings.filterwarnings('ignore')



def krwusd() -> dict:
    url = 'https://finance.naver.com/marketindex/?tabSel=exchange#tab_section'
    get = requests.get(url, verify=False)
    bs = BeautifulSoup(get.text, 'html.parser')
    return {
        'value': bs.select('span.value')[0].text,
        'change': bs.select('span.change')[0].text
    }

def index() -> dict:
    url = 'https://finance.naver.com/sise/'
    get = requests.get(url, verify=False)
    print(get.text)
    return {}

print(krwusd())
print(index())
