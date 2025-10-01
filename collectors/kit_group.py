import requests
from bs4 import BeautifulSoup

from collectors.collector import Collector


class KitGroupCollector(Collector):
    def collect(self, currencies_code: dict[str, int]):
        target_currency = 'UAH'
        result = {}
        resp = requests.get(self.url).text
        html = resp
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find('div', class_='currencies2__block1-wrapper')
        table = div.find_all('table')
        tbody = table[0].find('tbody')
        rows = tbody.find_all('tr', class_=lambda x: x != "tr-hidden")
        for row in rows:
            name = row.find('td').string
            if not name.startswith('Курс') or name[name.find('/')+1:] != target_currency:
                continue
            rates = row.find_all('a')
            name = name[name.find(' ')+1: name.find('/')].lower()
            if name in currencies_code:
                result[currencies_code[name]] = {
                    'sale': int(float(rates[1].string) * 100),
                    'pay': int(float(rates[0].string) * 100),
                }

        return result
