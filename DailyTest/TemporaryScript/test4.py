import datetime

a = str(datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday() + 7))[0:10]
b = str(datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday() + 3))[0:10]
c = datetime.datetime.now().weekday() + 7
print(a)
print(b)
print(c)
