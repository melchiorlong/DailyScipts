import pandas as pd
import os

file_path = '/Users/tianlong/Downloads/excel2/'
# file_path = '/Users/tianlong/Downloads/folder1/'
file_new_path = '/Users/tianlong/Downloads/folder3/'

delete_columns_1 = [
	'ExperimentName',
	'Subject',
	'Session',
	'Clock.Information',
	'DataFile.Basename',
	'Display.RefreshRate',
	'ExperimentVersion',
	'Group',
	'RandomSeed',
	'RuntimeVersion',
	'SessionDate',
	'SessionStartDateTimeUtc',
	'SessionTime',
	'StudioVersion',
	'TestMode',
	'Block11Practist',
	'Block11Practist.Cycle',
	'Block11Practist.Sample',
	'Block1Practist',
	'Block1Practist.Cycle',
	'Block1Practist.Sample',
	'Block1Practist1',
	'Block1Practist1.Cycle',
	'Block1Practist1.Sample',
	'Block1Practist2',
	'Block1Practist2.Cycle',
	'Block1Practist2.Sample',
	'List1',
	'list11',
	'List2',
	'list22',
	'List4',
	'List5',
	'List7',
	'List8',
	'Procedure[Block]',
	'Running[Block]',
	'type',
	'Trial',
	'List10',
	'List10.Cycle',
	'List10.Sample',
	'List3',
	'List3.Cycle',
	'List3.Sample',
	'List6',
	'List6.Cycle',
	'List6.Sample',
	'List9',
	'List9.Cycle',
	'List9.Sample',
	'picture',
	'Procedure[Trial]',
	'Running[Trial]',
	'Slide1.ACC',
	'Slide1.CRESP',
	'Slide1.DurationError',
	'Slide1.OnsetDelay',
	'Slide1.OnsetTime',
	'Slide1.OnsetToOnsetTime',
	'Slide1.RESP',
	'Slide1.RT',
	'Slide1.RTTime',
	'Slide2.ACC',
	'Slide2.CRESP',
	'Slide2.DurationError',
	'Slide2.OnsetDelay',
	'Slide2.OnsetTime',
	'Slide2.OnsetToOnsetTime',
	'Slide2.RESP',
	'Slide2.RT',
	'Slide2.RTTime',
	'Slide3.DurationError',
	'Slide3.OnsetDelay',
	'Slide3.OnsetTime',
	'Slide3.OnsetToOnsetTime',
	'Slide4.DurationError',
	'Slide4.OnsetDelay',
	'Slide4.OnsetTime',
	'Slide4.OnsetToOnsetTime',
]
delete_columns_2 = [
	'ExperimentName',
	'Subject',
	'Session',
	'Clock.Information',
	'DataFile.Basename',
	'Display.RefreshRate',
	'ExperimentVersion',
	'Group',
	'RandomSeed',
	'RuntimeVersion',
	'SessionDate',
	'SessionStartDateTimeUtc',
	'SessionTime',
	'StudioVersion',
	'TestMode',
	'Block11Practist',
	'Block11Practist.Cycle',
	'Block11Practist.Sample',
	'Block1Practist',
	'Block1Practist.Cycle',
	'Block1Practist.Sample',
	'Block1Practist1',
	'Block1Practist1.Cycle',
	'Block1Practist1.Sample',
	'Block1Practist2',
	'Block1Practist2.Cycle',
	'Block1Practist2.Sample',
	'List1',
	'list11',
	'List2',
	'list22',
	'List4',
	'List5',
	'List7',
	'List8',
	'Procedure[Block]',
	'Running[Block]',
	'type',
	'Trial',
	'List10',
	'List10.Cycle',
	'List10.Sample',
	'List3',
	'List3.Cycle',
	'List3.Sample',
	'List6',
	'List6.Cycle',
	'List6.Sample',
	'List9',
	'List9.Cycle',
	'List9.Sample',
	'picture',
	'Procedure[Trial]',
	'Running[Trial]',
	'Slide1.ACC',
	'Slide1.CRESP',
	'Slide1.DurationError',
	'Slide1.OnsetDelay',
	'Slide1.OnsetTime',
	'Slide1.OnsetToOnsetTime',
	'Slide1.RESP',
	'Slide1.RT',
	'Slide1.RTTime',
	'Slide2.ACC',
	'Slide2.CRESP',
	'Slide2.DurationError',
	'Slide2.OnsetDelay',
	'Slide2.OnsetTime',
	'Slide2.OnsetToOnsetTime',
	'Slide2.RESP',
	'Slide2.RT',
	'Slide2.RTTime',
	'Slide3.CRESP',
	'Slide3.DurationError',
	'Slide3.OnsetDelay',
	'Slide3.OnsetTime',
	'Slide3.OnsetToOnsetTime',
	'Slide4.CRESP',
	'Slide4.DurationError',
	'Slide4.OnsetDelay',
	'Slide4.OnsetTime',
	'Slide4.OnsetToOnsetTime',
]
reserve_columns = [
	'Block',
	'ans',
	'word',
	'word1',
	'word2',
	'Slide3.ACC',
	'Slide3.RESP',
	'Slide3.RT',
	'Slide4.ACC',
	'Slide4.RESP',
	'Slide4.RT',
]


def excel_columns_operate(operation: str, column_list: list):
	for dir_path, dir_names, filenames in os.walk(file_path):
		for file_name in filenames:
			if 'xls' in file_name:
				df = pd.read_excel(file_path + file_name, header=0)
				if operation == 'delete':
					df.drop(column_list, axis=1, inplace=True)
				elif operation == 'reserve':
					df = df[column_list]

				# df = df.fillna("NULL")
				new_file_name = file_new_path + file_name + 'x'
				df.to_excel(new_file_name, index=False, engine='openpyxl')


def columns_calc():
	# fp = '/Users/tianlong/Downloads/folder2/'
	res_list = []
	for dir_path, dir_names, filenames in os.walk(file_new_path):
		for file_name in filenames:
			if 'xlsx' in file_name and '~' not in file_name:
				df = pd.read_excel(file_new_path + file_name, header=0)
				ans_slide3_resp_j_count = 0
				ans_slide3_resp_none_count = 0
				ans_slide4_resp_j_count = 0
				ans_slide4_resp_none_count = 0
				slide3_rt_list =[]
				slide4_rt_list =[]
				for index, row in df.iterrows():
					if row['ans'] == 'j' and row['Slide3.RESP'] == 'j':
						ans_slide3_resp_j_count += 1
						slide3_rt_list.append(row['Slide3.RT'])
					if row['ans'] is None and row['Slide3.RESP'] is None:
						ans_slide3_resp_none_count += 1
					if row['ans'] == 'j' and row['Slide4.RESP'] == 'j':
						ans_slide4_resp_j_count += 1
						slide4_rt_list.append(row['Slide4.RT'])
					if row['ans'] is None and row['Slide4.RESP'] is None:
						ans_slide4_resp_none_count += 1
				p1_hit_rate = ans_slide3_resp_j_count * 1.0 / 20
				p1_rejection_rate = ans_slide3_resp_none_count * 1.0 / 20
				p2_hit_rate = ans_slide4_resp_j_count * 1.0 / 20
				p2_rejection_rate = ans_slide4_resp_none_count * 1.0 / 20
				slide3_rt_list_int = list(map(lambda x: int(x), slide3_rt_list))
				slide4_rt_list_int = list(map(lambda x: int(x), slide4_rt_list))
				p1_correct_reaction_avg = sum(slide3_rt_list_int) / len(slide3_rt_list_int) if len(slide3_rt_list_int) else None
				p2_correct_reaction_avg = sum(slide4_rt_list_int) / len(slide4_rt_list_int) if len(slide4_rt_list_int) else None


			# def j_count(columns: list):
			# 	fac_count = 0
			# 	for fac in columns:
			# 		if fac == 'j':
			# 			fac_count += 1
			# 	return fac_count *1.0 / 20
			#
			# ans_count = j_count(df['ans'])
			# slide3_cresp_count = j_count(df['Slide3.CRESP'])
			# slide3_resp_count = j_count(df['Slide3.RESP'])
			# slide4_cresp_count = j_count(df['Slide4.CRESP'])
			# slide4_resp_count = j_count(df['Slide4.RESP'])
			#
				dict_1 = {
					file_name: {
						'P1击中个数': ans_slide3_resp_j_count,
						'P1正确否定个数': ans_slide3_resp_none_count,
						'P1命中率': p1_hit_rate,
						'P1否定率': p1_rejection_rate,
						'P1正确反应时': p1_correct_reaction_avg,
						'P2击中个数': ans_slide4_resp_j_count,
						'P2正确否定个数': ans_slide4_resp_none_count,
						'P2命中率': p2_hit_rate,
						'P2否定率': p2_rejection_rate,
						'P2正确反应时': p2_correct_reaction_avg,
					},
				}
				res_list.append(dict_1)
	return res_list


def result_write(result_list: list):
	res_date_frame = pd.DataFrame()
	for file_res in result_list:
		for file_name, res_dict in file_res.items():
			data = {}
			for j_name, j_count in res_dict.items():
				data['file_name'] = [file_name]
				data[j_name] = [j_count]
			df = pd.DataFrame(data)
			res_date_frame = pd.concat([res_date_frame, df], ignore_index=True)
	res_file_name = '/Users/tianlong/Downloads/result.xlsx'
	res_date_frame.to_excel(res_file_name, index=False, engine='openpyxl')

res = columns_calc()
result_write(res)

# excel_columns_operate('reserve', reserve_columns)
