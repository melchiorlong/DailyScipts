import pandas as pd
import numpy as np
import os

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
file_path = '/Users/tianlong/Downloads/excel2/'
for dir_path, dir_names, filenames in os.walk(file_path):
	for file_name in filenames:
		if 'xls' in file_name:
			df = pd.read_excel(file_path + file_name, header=0, keep_default_na=False)
			df1 = df[reserve_columns]
			print(df1)