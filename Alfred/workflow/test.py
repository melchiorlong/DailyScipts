import keyword

keyword_list = keyword.kwlist

query_str = '    res return '

if len(query_str) <= 0:
	raise ValueError
stripped_str = query_str.strip().lower()
if stripped_str in list(keyword_list):
	raise ValueError
res = stripped_str.replace(' ', '_')

print(res)