import requests

from collectors.collector import Collector


class NationalBankOfUkraineCollector(Collector):
    def collect(self, currencies_code: dict[str, int]):
        resp = requests.get(self.url)
        result = {}
        for line in resp.json():
            if line['cc'].lower() not in currencies_code:
                continue
            result[currencies_code[line['cc'].lower()]] = {
                'sale': int(float(line['rate']) * 100),
                'pay': int(float(line['rate']) * 100)
            }

        return result
