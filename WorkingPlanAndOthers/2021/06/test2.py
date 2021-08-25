from datetime import date, timedelta, datetime

_date_start = date(2021, 7, 20)
_date_end = date(2021, 8, 19)
_date_step = 3

# for i in range(0 ,(_date_end - _date_start).days + 1, _date_step):
#     day = _date_start + timedelta(days=i)
#     day_str = day.strftime('%Y-%m-%d')
#     day_tail = day + timedelta(days=_date_step)
#     day_tail_str = day_tail.strftime('%Y-%m-%d')
#     print("day_str "+day_str)
#     print("day_tail_str "+day_tail_str)



d = date(2021, 7, 20)
# day = d + timedelta(days=-1)

print((d + timedelta(days=-1)).strftime('%Y-%m-%d'))