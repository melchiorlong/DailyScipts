import pandas as pd
import os

# file_path = '/Users/tianlong/Downloads/excel/'
file_path = '/Users/tianlong/Downloads/folder1/'
file_new_path = '/Users/tianlong/Downloads/folder2/'

l1 = [
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

for dir_path, dir_names, filenames in os.walk(file_path):
	for file_name in filenames:
		if 'xls' in file_name:
			df = pd.read_excel(file_path + file_name, header=0)
			# A - O，R - AN，AR - BY，CB - CE，CK - CN
			df.drop(l1, axis=1, inplace=True)
			# df = df.fillna("NULL")
			new_file_name = file_new_path + file_name+ 'x'
			df.to_excel(new_file_name, index=False, engine='openpyxl')

