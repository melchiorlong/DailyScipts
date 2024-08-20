from datetime import datetime, timedelta

s1 = '04:57:00'



d1 = datetime.strptime(s1, '%H:%M:%S')

d2 = d1 + timedelta(hours=0 * 24)

print(d1)
print(d2)


s2 = 'T+1'
print(s2[0])

print(datetime.now().strftime('_%H:%M:%S'))

# print(str().replace(' ', '_'))
