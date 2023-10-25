import pandas as pd
import os

file_path = '/Users/tianlong/Downloads/excel2/'
# file_path = '/Users/tianlong/Downloads/folder1/'
file_new_path = '/Users/tianlong/Downloads/folder3/'
for dir_path, dir_names, filenames in os.walk(file_new_path):
	for file_name in filenames:
		if 'xlsx' in file_name and '~' not in file_name:
			df = pd.read_excel(file_new_path + file_name, header=0)
			print(df.columns)
			# if 'ans' in df.index():
			# 	print(file_name)