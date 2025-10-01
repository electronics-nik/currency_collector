from bs4 import BeautifulSoup

from collectors.collector import Collector
from collectors.web_utils import get_html


class RaiffeisenBankAvalCollector(Collector):
    def collect(self, currencies_code: dict[str, int]):
        result = {}
        html = get_html(self.url, class_='bank-info__table-body')
        soup = BeautifulSoup(html, 'lxml')
        rows = soup.find('div', class_='bank-info__table-body').find_all('div', class_='bank-info__table-row')
        for row in rows:
            values = [item.string.lower().strip() for item in row.find_all('div', class_='bank-info__table-column')]
            if values[0] not in currencies_code:
                continue
            result[currencies_code[values[0]]] = {
                'sale': int(float(values[2]) * 100),
                'pay': int(float(values[1]) * 100)
            }

        return result
