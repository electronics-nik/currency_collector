import requests

from collectors.collector import Collector


class PrivatBankCollector(Collector):
    def collect(self, currencies_code: dict[str, int]) -> dict[int, dict[str, int]]:
        resp = requests.get(self.url)
        result = {}
        for line in resp.json():
            if line['base_ccy'] != 'UAH' and line['ccy'].lower() not in currencies_code:
                continue
            result[currencies_code[line['ccy'].lower()]] = {
                'sale': int(float(line['sale']) * 100),
                'pay': int(float(line['buy']) * 100),
            }

        return result
