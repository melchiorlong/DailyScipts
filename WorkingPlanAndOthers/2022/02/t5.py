from datetime import datetime



time1 = datetime.fromisoformat('2022-03-01T08')

print(time1)

print(time1.strftime('%Y-%m-%d %H:%M:%S'))
