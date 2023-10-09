import os
import sys
from datetime import date

import requests
import json

cur_str = sys.argv[1]
if '!' in cur_str:
	cur_str = cur_str.replace('!', '')
	cur = cur_str.split('/')[0].strip()
	amount = cur_str.split('/')[1].strip()
	current_path = os.getcwd()
	today_date_str = str(date.today())
	file_name = 'Rates_' + today_date_str + '.txt'
	temp_file_abspath = current_path + '/' + file_name


	def create_item(title, subtitle, icon, arg):
		item = {}
		item['title'] = title
		item['subtitle'] = subtitle
		item['icon'] = icon
		item['arg'] = arg
		return item


	def get_rates():
		for dirpath, dirnames, filenames in os.walk(current_path):
			if file_name in filenames:
				with open(file=temp_file_abspath, mode='r', encoding='utf-8') as f:
					raw_json = f.read()
				json_map = json.loads(raw_json)
				return json_map['conversion_rates']

			else:
				currency_rate_api = 'https://v6.exchangerate-api.com/v6/767a1945568cb2d3c4685de0/latest/CNY'
				currency_json = requests.get(currency_rate_api).text
				with open(file=temp_file_abspath, mode='w', encoding='utf-8') as f:
					f.write(currency_json)
				json_map = json.loads(currency_json)
				return json_map['conversion_rates']


	currency_map = get_rates()
	if cur.upper() in currency_map.keys():
		rate = currency_map.get(cur.upper(), 1)
		cny_amount = float(amount) * 1.0 / rate
		items = [create_item(
			str(cny_amount),
			'人民币',
			{},
			str(cny_amount),
		)]
		result = {'items': items}
		print(json.dumps(result))
