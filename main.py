from db_connector import Connector
from collectors.plugin_loader import CollectorLoader

conn = Connector()


def store_result_to_db(bank_id: int, data: dict[int, dict[str, int]]):
    for idx, values in data.items():
        sql = f'''insert into currency_rate(
            bank_id,
            currency_id,
            sale,
            pay
        ) values (
            {bank_id},
            {idx},
            {values['sale']},
            {values['pay']}
        ) returning id;'''

        conn.insert(sql)


def go_collect():
    sql = 'select id, bank_currency_name from currency where is_active;'
    currencies = {}
    for id_currency, name in conn.select(sql):
        currencies[name.lower()] = id_currency

    sql = '''
          select b.id,
                 b.name_ua,
                 ba.url,
                 ba.module_name,
                 ba.class_name
            from bank as b
            join bank_api as ba on b.id = ba.bank_id
           where b.is_active
           order by b.id;
          '''
    for bank_id, bank_name, bank_url_api, m_name, c_name in conn.select(sql):
        print(bank_id, bank_name, m_name, c_name)

        loader = CollectorLoader(m_name)
        obj = loader.create_instance(c_name, bank_url_api)
        res = obj.collect(currencies)
        print(res)
        store_result_to_db(bank_id, res)


if __name__ == '__main__':
    go_collect()
