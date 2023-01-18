from datetime import datetime

str = '28/Feb/2019:13:17:10 +0000'



date = '2022-04-01'
d2 = datetime.now()
print(d2)

d3 = d2.strftime('%d/%b/%Y:%H:%M:%S %tzone')

date_str = str.split('+')[0].strip()
d = datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S')
print(d)
print(d3)
