# date, num1, num2, num3
from datetime import datetime, timedelta
import pandas as pd

# print(datetime.now().strftime('%Y-%m-%d %H:00:00'))

day_list = []
num1_list = []
num2_list = []
num3_list = []
i, j, k = 100000, 200000, 300000
day = datetime.now()
day_step = 1

for row in range(10000000):
    num1_list.append(i)
    num2_list.append(j)
    num3_list.append(k)
    day_list.append(day)

    i = i + 1
    j = j + 1
    k = k + 1
    if day_step <= 3:
        day = day + timedelta(days=1)
        day_step = day_step + 1
    else:
        day_step = 1
        day = datetime.now()

datetime_list = [f.strftime('%Y-%m-%d %H:00:00') for f in day_list]

data = {
    'datetime': datetime_list,
    'num1_list': num1_list,
    'num2_list': num2_list,
    'num3_list': num3_list,
}

pd.DataFrame(data).to_csv('data.csv', index=False)

l1 = ['2024-08-10', '2024-08-11', '2024-08-09', '2024-08-07', '2024-08-08', ]
