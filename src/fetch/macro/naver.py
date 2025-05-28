from bs4 import BeautifulSoup
import requests, warnings
warnings.filterwarnings('ignore')



def krwusd() -> dict:
    url = 'https://finance.naver.com/marketindex/?tabSel=exchange#tab_section'
    get = requests.get(url, verify=False)
    bs = BeautifulSoup(get.text, 'html.parser')
    value = bs.select('span.value')[0].text
    change = bs.select('span.change')[0].text
    curr = float(value.replace(",", ""))
    date = bs.select('span.time')[0].text.split(" ")[0].replace(".", "-")
    prev = curr - float(change) if bs.select('span.blind')[0].text == '하락' else curr + float(change)
    pct = 100 * ((curr / prev) - 1)
    return {
        'value': curr,
        'change': round(pct, 2),
        'date': date
    }


if __name__ == "__main__":

    print(krwusd())