from datetime import datetime, timedelta
import re



start_date_dt = datetime.strptime('2021-10-01', '%Y-%m-%d')
end_date_dt = datetime.strptime('2021-10-02', '%Y-%m-%d')


print((start_date_dt - end_date_dt).days)


print((end_date_dt + timedelta(days=-30)).strftime('%Y-%m-%d'))


#
# if (end_date_dt > start_date_dt):
#     print(1)
# else:
#     print(0)
#



#
#
#
#
#
# string1 = """
#         google.protobuf.Int32Value kch_dnu = 4;
#         google.protobuf.Int32Value kch_day1_install = 5;
#         google.protobuf.Int32Value kch_day1_retention = 6;
#         google.protobuf.BoolValue kch_day1_retention_ge_3 = 7;
#         google.protobuf.Int32Value kch_day2_install = 8;
#         google.protobuf.Int32Value kch_day2_retention = 9;
#         google.protobuf.BoolValue kch_day2_retention_ge_3 = 10;
#         google.protobuf.Int32Value kch_day3_install = 11;
#         google.protobuf.Int32Value kch_day3_retention = 12;
#         google.protobuf.BoolValue kch_day3_retention_ge_3 = 13;
#         google.protobuf.Int32Value kch_day7_install = 14;
#         google.protobuf.Int32Value kch_day7_retention = 15;
#         google.protobuf.BoolValue kch_day7_retention_ge_3 = 16;
#         google.protobuf.Int32Value kch_day14_install = 17;
#         google.protobuf.Int32Value kch_day14_retention = 18;
#         google.protobuf.BoolValue kch_day14_retention_ge_3 = 19;
#         google.protobuf.Int32Value kch_day30_install = 20;
#         google.protobuf.Int32Value kch_day30_retention = 21;
#         google.protobuf.BoolValue kch_day30_retention_ge_3 = 22;
# """
#
# # re.sub('\s\d{1,}', repl, string1, count=0, flags=0)
# #
# # string1.reg
#
#
# pattern = re.compile(r'\s\d{1,}')   # 查找数字
# result1 = pattern.findall(string1)
# print(result1)