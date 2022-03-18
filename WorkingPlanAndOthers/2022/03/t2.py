from datetime import datetime

#
# datetime.utcnow()
# print(datetime.weekday(datetime.utcnow()) + 1)


# t1 = datetime.utcfromtimestamp(int(1647742393))
# print(t1)

factor_list = ['asdas', '']
factors = list(filter(None, factor_list))
print(factors)



s1 = 's3://gvprod/devops/dw/ua_export/google/uac3/2022-03-16/aiolos_gp/data000'
print("/".join(s1.split('/')[:-1]))
# 's3://gvprod/devops/dw/ua_export/google/day7_good30/2022-03-15/aiolos_gp'