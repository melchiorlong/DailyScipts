import csv
import json

csv_file = 'raw_data.csv'
json_file = 'output.json'


def build_tree(data, levels):
	if len(levels) == 0:
		return []

	current_level = levels.pop(0)
	grouped_data = {}
	for row in data:
		key = row[current_level]
		if key not in grouped_data:
			grouped_data[key] = []

		grouped_data[key].append(row)

	children = []
	for key, values in grouped_data.items():
		child = {"name": key}
		child["children"] = build_tree(values, levels.copy())
		children.append(child)

	return children


with open(file=csv_file, mode='r', encoding='utf-8-sig') as file:
	reader = csv.reader(file)
	data = []
	for row in reader:
		data.append(row)

	levels = list(range(len(data[0])))

	final_json = json.dumps(
		{
			"name": "指标",
			"children": build_tree(data, levels)
		},
		indent=4,
		ensure_ascii=False
	)

with open(file=json_file, mode='w', encoding='utf-8') as file:
	file.write(final_json)
