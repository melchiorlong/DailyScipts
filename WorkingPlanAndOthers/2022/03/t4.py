from datetime import datetime

# def get_hour_range(hour_start, hour_end):
#     """
#     :return: 返回从hour_start到hour_end的所有小时的列表
#     """
#     dates = []
#     dt = datetime.datetime.strptime(hour_start, "%Y-%m-%dT%H")
#     dt_end = datetime.datetime.strptime(hour_end, "%Y-%m-%dT%H")
#     while dt <= dt_end:
#         dates.append(dt.strftime("%Y-%m-%dT%H"))
#         dt = dt + datetime.timedelta(hours=1)
#     return dates

log_time = datetime.fromisoformat('2022-03-01_01:01:01')
print(log_time)