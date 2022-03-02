from datetime import datetime, timedelta



# time1 = datetime.fromisoformat('2022-03-01T08')

# print(time1)
#
# print(time1.strftime('%Y-%m-%d %H:%M:%S'))



end_time = datetime.utcnow().strftime('%H-%M')

da1 = datetime.strptime(end_time, '%H-%M')

print(da1)