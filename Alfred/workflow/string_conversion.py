# String conversion
import json
import sys
import keyword

query_str = sys.argv[1:]
keyword_list = keyword.kwlist


def create_item(title, subtitle, icon, arg):
	item = {
		'title': title,
		'subtitle': subtitle,
		'icon': icon,
		'arg': arg}
	return item


items = []

try:
	if len(query_str) <= 0:
		raise ValueError
	stripped_str_list = list(map(lambda x: str(x).lower().strip(), query_str))
	if len(stripped_str_list) == 1 and stripped_str_list[0] in list(keyword_list):
		raise ValueError
	res = '_'.join(stripped_str_list)
	items.append(
		create_item(
			res,
			'下划线命名',
			{},
			res
		)
	)
except ValueError:
	items.append(
		create_item('Invalid input', '不能输入Python关键字', {'type': 'default', 'path': 'icon.png'}, ''))

result = {'items': items}

print(json.dumps(result))
