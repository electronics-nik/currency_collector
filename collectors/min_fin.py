import requests
from bs4 import BeautifulSoup

from collectors.collector import Collector


class MinFineCollector(Collector):
    def collect(self, currencies_code: dict[str, int]):
        result = {}
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'lxml')
        rows = soup.find_all('tr', class_='sc-1x32wa2-4')
        for row in rows:
            currency = row.find('a', class_='sc-1x32wa2-7 ciClTw')
            if not currency or currency.string.lower() not in currencies_code:
                continue
            values = row.find_all('div', class_='sc-1x32wa2-9 bKmKjX')[:2]

            result[currencies_code[currency.string.lower()]] = {
                'sale': int(float(values[1].find(string=True, recursive=False).strip().replace(',', '.')) * 100),
                'pay': int(float(values[0].find(string=True, recursive=False).strip().replace(',', '.')) * 100)
            }

        return result
