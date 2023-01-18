#!/opt/anaconda3/bin/python3
# encoding: utf-8

import sys
import requests
import json
from workflow import Workflow3


def main():
    wf = Workflow3()
    cur_str = sys.argv[1]
    cur = cur_str.split(',')[0].strip()
    amount = cur_str.split(',')[1].strip()
    currency_rate_api = 'https://api.exchangerate-api.com/v4/latest/CNY'
    currency_json = requests.get(currency_rate_api).text
    json_map = json.loads(currency_json)
    currency_map = json_map['rates']

    if cur.upper() in currency_map.keys():
        rate = currency_map.get(cur.upper(), 1)
        cny_amount = float(amount) * 1.0 / rate

        kwargs = {
            'title': cny_amount,
            "valid": True,
            'arg': cny_amount,
        }
        wf.add_item(**kwargs)
        wf.send_feedback()
    else:
        kwargs = {
            'title': "Error",
            "valid": False,
        }
        wf.add_item(**kwargs)
        wf.send_feedback()


if __name__ == '__main__':
    main()
