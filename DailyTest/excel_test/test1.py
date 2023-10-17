import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

excel_path = '~/Downloads/data_template.xlsx'
# df = pd.read_excel(excel_path, index_col=1)
df = pd.read_excel(excel_path)


# 1.每个指标的组内均值；
def avg_in_group():
	for col_name in df.columns:
		if 'indicator' in col_name:
			res = df.groupby('group')[col_name].mean()
			print(res)


# 2.每个指标的整体均值；
def avg_per_indicators():
	for col_name in df.columns:
		if 'indicator' in col_name:
			res = df[col_name].mean()
			print(res)


# 3.每个城市大于组内均值的指标，小于组内均值的指标；
def inner_group_comparison():
	df_temp = df

	def get_group_avg_df():
		res_df = pd.DataFrame()
		for col_name in df.columns:
			if 'indicator' in col_name:
				res = df_temp.groupby('group')[col_name].mean()
				res_df.insert(0, col_name, res)
		return res_df

	group_avg_df = get_group_avg_df()

	res_less_list = []
	res_greater_list = []
	for index, row in df_temp.iterrows():
		city = row['city']
		group = row['group']
		less_list = []
		less_dict = {}
		greater_list = []
		greater_dict = {}

		for col in df.columns[2:]:
			if row[col] >= group_avg_df.loc[group, col]:
				greater_list.append(col)
				greater_dict[city] = greater_list
				res_greater_list.append(greater_dict)
			elif row[col] < group_avg_df.loc[group, col]:
				less_list.append(col)
				less_dict[city] = less_list
				res_less_list.append(less_dict)

	print("大于等于组内均值" + str(res_greater_list))
	print("小于组内均值" + str(res_less_list))


# 4.每个城市大于全行均值的指标，小于全行均值的指标

def full_scope_comparison():
	res_dict = {}
	df_temp = df
	for col_name in df.columns:
		if 'indicator' in col_name:
			res = df[col_name].mean()
			res_dict[col_name] = res

	res_less_list = []
	res_greater_list = []
	for index, row in df_temp.iterrows():
		city = row['city']
		less_list = []
		less_dict = {}
		greater_list = []
		greater_dict = {}
		less_list.append('indicator_1') if row['indicator_1'] <= res_dict['indicator_1'] else greater_list.append(
			'indicator_1')
		less_list.append('indicator_2') if row['indicator_2'] <= res_dict['indicator_2'] else greater_list.append(
			'indicator_2')
		less_list.append('indicator_3') if row['indicator_3'] <= res_dict['indicator_3'] else greater_list.append(
			'indicator_3')
		less_list.append('indicator_4') if row['indicator_4'] <= res_dict['indicator_4'] else greater_list.append(
			'indicator_4')
		less_list.append('indicator_5') if row['indicator_5'] <= res_dict['indicator_5'] else greater_list.append(
			'indicator_5')
		less_dict[city] = less_list
		greater_dict[city] = greater_list
		res_less_list.append(less_dict)
		res_greater_list.append(greater_dict)

	print(res_less_list)
	print(res_greater_list)


inner_group_comparison()
