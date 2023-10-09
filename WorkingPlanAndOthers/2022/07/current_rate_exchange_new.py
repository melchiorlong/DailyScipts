import sys
import requests
import json

cur_str = sys.argv[1]
if '!' in cur_str:
	cur_str = cur_str.replace('!', '')
	cur = cur_str.split('/')[0].strip()
	amount = cur_str.split('/')[1].strip()

	def create_item(title, subtitle, icon, arg):
		item = {}
		item['title'] = title
		item['subtitle'] = subtitle
		item['icon'] = icon
		item['arg'] = arg
		return item

	def get_rate():
		currency_rate_api = 'https://v6.exchangerate-api.com/v6/767a1945568cb2d3c4685de0/latest/CNY'
		currency_json = requests.get(currency_rate_api).text
		json_map = json.loads(currency_json)
		return json_map['conversion_rates']


	currency_map = get_rate()
	if cur.upper() in currency_map.keys():
		rate = currency_map.get(cur.upper(), 1)
		cny_amount = float(amount) * 1.0 / rate
		items = []
		items.append(create_item(
			str(cny_amount),
			'人民币',
			{},
			str(cny_amount),
		))
		result = {}
		result['items'] = items
		print(json.dumps(result))
