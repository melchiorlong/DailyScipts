import requests as r
import time
from datetime import datetime
import json
from chapter_list_local import chapter_list_local


class BookReadingWord:

	def __init__(self, real_name, job_number):
		self.real_name = real_name
		self.job_number = job_number

	def reading_login(self, real_name, job_number):
		post_data = {
			'real_name': real_name,
			'job_number': job_number
		}

		login_resp = r.post(
			url='https://bank.tizireading.com/api/Login/login',
			data=post_data
		)
		resp_json = login_resp.text
		resp_dict = json.loads(resp_json)

		print(resp_dict)

		login_info_dict = {
			'token': resp_dict['retval']['token'],
			'user_id': resp_dict['retval']['user_id'],
			'sign': resp_dict['retval']['sign'],
			'timestamp': resp_dict['retval']['timestamp']
		}

		return login_info_dict

	def reading_sign_in(self, login_info_dict):

		sign_in_url = 'http://bank.tizireading.com/api/Sign_In/signIn'

		sign_in_params = {
			'token': login_info_dict['token'],
			'user_id': login_info_dict['user_id'],
			'sign': login_info_dict['sign'],
			'timestamp': login_info_dict['timestamp'],
		}
		sign_resp = r.get(
			url=sign_in_url,
			params=sign_in_params
		)
		print(sign_resp.text)

	def get_chapter_list(self, login_info_dict):

		# get_chapter_list_url = 'http://bank.tizireading.com/api/Book/getChapterLists'
		# get_chapter_list_data = {
		# 	'book_no': 86828969,
		# 	'token': login_info_dict['token'],
		# 	'user_id': login_info_dict['user_id'],
		# 	'sign': login_info_dict['sign'],
		# 	'timestamp': login_info_dict['timestamp'],
		# }

		# req_headers = {
		# 	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
		#
		# get_chapter_list_resp = r.get(
		# 	url=get_chapter_list_url,
		# 	params=get_chapter_list_data,
		# 	headers=req_headers,
		# )
		# get_chapter_dict = {}
		# try:
		# 	get_chapter_dict = json.loads(str(get_chapter_list_resp.text))
		# except:
		# 	print("json错误")

		get_chapter_dict = json.loads(chapter_list_local)
		chapter_dict = {}
		if len(get_chapter_dict) > 0:
			for retval_fac in get_chapter_dict['retval']:
				chapter_dict[retval_fac['id']] = retval_fac['toc_href']
		return chapter_dict

	def reading_start(self, login_info_dict, chapter_id):

		get_url = 'http://bank.tizireading.com/api/Book/startRead'
		data_dict = {
			'chapter_id': chapter_id,
			'token': login_info_dict['token'],
			'user_id': login_info_dict['user_id'],
			'sign': login_info_dict['sign'],
			'timestamp': login_info_dict['timestamp'],
		}

		reading_start_resp = r.get(
			url=get_url,
			params=data_dict
		)
		reading_start_resp_dict = json.loads(reading_start_resp.text)
		resp_no = reading_start_resp_dict['retval']['no']
		return resp_no

	def reading_end(self, login_info_dict, last_update_sign, resp_no):

		reading_end_url = 'http://bank.tizireading.com/api/Book/endRead'
		reading_end_data = {
			'no': resp_no,
			'last_update_sign': last_update_sign,
			'token': login_info_dict['token'],
			'user_id': login_info_dict['user_id'],
			'sign': login_info_dict['sign'],
			'timestamp': login_info_dict['timestamp'],
		}

		r.post(
			url=reading_end_url,
			data=reading_end_data
		)

	def get_monitor_data(self, login_info_dict, last_update_sign, resp_no):
		monitor_data = {
			"no": resp_no,
			"last_update_sign": last_update_sign,
			"token": login_info_dict['token'],
			"user_id": login_info_dict['user_id'],
			"sign": login_info_dict['sign'],
			"timestamp": login_info_dict['timestamp']
		}
		return monitor_data

	def post_monitor(self, login_info_dict, last_update_sign, resp_no):
		monitor_resp = r.post(
			url='https://bank.tizireading.com/api/Book/monitorRead',
			json=self.get_monitor_data(login_info_dict, last_update_sign, resp_no),
		)
		print(monitor_resp.text)

	def run(self):
		login_info_dict = self.reading_login(self.real_name, self.job_number)
		# self.reading_sign_in(login_info_dict)
		chapter_dict = self.get_chapter_list(login_info_dict)

		for chapter_id in chapter_dict.keys():
			print("chapter_id: " + str(chapter_id))
			last_update_sign = chapter_dict[chapter_id]
			resp_no = self.reading_start(login_info_dict, chapter_id)
			resp_times = 0
			while True:
				if resp_times > 24:
					break
				self.post_monitor(login_info_dict, last_update_sign, resp_no)
				resp_times += 1
				print('当前进程用户: ' + self.real_name)
				print('当前时间: ' + str(datetime.now()))
				print('响应次数: ' + str(resp_times))
				time.sleep(5)

			self.reading_end(login_info_dict, last_update_sign, resp_no)
