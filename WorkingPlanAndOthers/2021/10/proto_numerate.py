prote_str = """
            google.protobuf.Int32Value kch_day1_install = 2;
            google.protobuf.Int32Value kch_day1_retention = 3;
            google.protobuf.BoolValue kch_day1_retention_ge_3 = 4;         // 是否大于等于3天数据
            google.protobuf.Int32Value kch_day2_install = 5;
            google.protobuf.Int32Value kch_day2_retention = 6;
            google.protobuf.BoolValue kch_day2_retention_ge_3 = 7;
            google.protobuf.Int32Value kch_day3_install = 8;
            google.protobuf.Int32Value kch_day3_retention = 9;
            google.protobuf.BoolValue kch_day3_retention_ge_3 = 10;
            google.protobuf.Int32Value kch_day7_install = 11;
            google.protobuf.Int32Value kch_day7_retention = 12;
            google.protobuf.BoolValue kch_day7_retention_ge_3 = 13;
            google.protobuf.Int32Value kch_day14_install = 14;
            google.protobuf.Int32Value kch_day14_retention = 15;
            google.protobuf.BoolValue kch_day14_retention_ge_3 = 16;
            google.protobuf.Int32Value kch_day30_install = 17;
            google.protobuf.Int32Value kch_day30_retention = 18;
            google.protobuf.BoolValue kch_day30_retention_ge_3 = 19;
"""

result_list = []
for index, line in enumerate(prote_str.strip().split('\n')):
    if line:
        res_line = line.split('=')[0] + '= ' + str(index + 1) + ';' + line.split('=')[1].split(';')[-1]
        result_list.append(res_line)

s = '\n'.join(result_list)
print(s)
