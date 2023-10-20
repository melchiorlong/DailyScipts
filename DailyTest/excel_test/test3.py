import pandas as pd

df = pd.read_excel('/Users/tianlong/Downloads/data_template.xlsx', index_col=0)
# print(df.loc['beijing', 'group'])

df.index.name = '城市'

for i in df.index:
	print(i)

# print(df.index)

# template = df['city'] == '上海'
# group_ser = df.loc[template]['group']
# print(group_ser)