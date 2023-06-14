import requests as r
import time
from datetime import datetime
import json

post_data = {
	'real_name': '田龙',
	'job_number': '22092063'
}

login_resp = r.post(
	url='https://bank.tizireading.com/api/Login/login',
	data=post_data
)
resp_json = login_resp.text

resp_dict = json.loads(resp_json)

print(resp_dict)

token = resp_dict['retval']['token']
user_id = resp_dict['retval']['user_id']
sign = resp_dict['retval']['sign']
timestamp = resp_dict['retval']['timestamp']


def get_monitor_data(last_update_sign):
	monitor_data = {
		"no": "64730b16a6317",
		"last_update_sign": last_update_sign,
		"token": token,
		"user_id": user_id,
		"sign": sign,
		"timestamp": timestamp
	}
	return monitor_data


def do_resp(last_update_sign):
	monitor_resp = r.post(
		url='https://bank.tizireading.com/api/Book/monitorRead',
		json=get_monitor_data(last_update_sign),
		cookies=''
	)
	print(monitor_resp.text)

resp_times = 0
last_update_sign_base = 0
run_flag = True
while run_flag:
	now_time = datetime.now()
	# tag = datetime.strptime('2023-05-27 08:00:00', '%Y-%m-%d %H:%M:%S')
	# if now_time >= tag:
	# 	run_flag = False
	# 	break
	current_ts = time.time()
	time_gap = 15 - (current_ts - int(current_ts))
	last_update_sign_base += time_gap
	do_resp(last_update_sign_base)
	resp_times += 1
	print('当前时间: ' + str(datetime.now()))
	print('响应次数: ' + str(resp_times))
	time.sleep(15)
