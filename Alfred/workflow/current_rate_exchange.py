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
	file_name = 'Rates.txt'
	rates_file_abspath = current_path + '/' + file_name


	def create_item(title, subtitle, icon, arg):
		item = {
			'title': title,
			'subtitle': subtitle,
			'icon': icon,
			'arg': arg
		}
		return item


	def api_request():
		currency_rate_api = 'https://v6.exchangerate-api.com/v6/767a1945568cb2d3c4685de0/latest/CNY'
		return requests.get(currency_rate_api).text


	def get_rates():
		for dir_path, dir_names, filenames in os.walk(current_path):
			if file_name not in filenames or os.path.getsize(rates_file_abspath) == 0:
				raw_json = api_request()
				with open(file=rates_file_abspath, mode='w', encoding='utf-8') as f:
					f.write(raw_json)
				return json.loads(raw_json)['conversion_rates']

			with open(file=rates_file_abspath, mode='r', encoding='utf-8') as f:
				raw_json = f.read()
				json_map = json.loads(raw_json)
			if date.today() != date.fromtimestamp(json_map.get('time_last_update_unix')):
				raw_json = api_request()
				with open(file=rates_file_abspath, mode='w', encoding='utf-8') as f:
					f.write(raw_json)
				json_map = json.loads(raw_json)

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
