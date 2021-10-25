prote_str = """
              google.protobuf.IntValue bj_date = 1;
        google.protobuf.IntValue retention_1d = 2;
        google.protobuf.IntValue retention_2d = 2;
        google.protobuf.IntValue retention_3d = 2;
        google.protobuf.IntValue retention_4d = 2;
        google.protobuf.IntValue retention_5d = 2;
        google.protobuf.IntValue retention_6d = 2;
        google.protobuf.IntValue retention_7d = 2;
        google.protobuf.IntValue retention_8d = 2;
        google.protobuf.IntValue retention_9d = 2;
        google.protobuf.IntValue retention_10 = 2;
        google.protobuf.IntValue retention_11 = 2;
        google.protobuf.IntValue retention_12 = 2;
        google.protobuf.IntValue retention_13 = 2;
        google.protobuf.IntValue retention_14 = 2;
        google.protobuf.IntValue retention_15 = 2;
        google.protobuf.IntValue retention_16 = 2;
        google.protobuf.IntValue retention_17 = 2;
        google.protobuf.IntValue retention_18 = 2;
        google.protobuf.IntValue retention_19 = 2;
        google.protobuf.IntValue retention_20 = 2;
        google.protobuf.IntValue retention_21 = 2;
        google.protobuf.IntValue retention_22 = 2;
        google.protobuf.IntValue retention_23 = 2;
        google.protobuf.IntValue retention_24 = 2;
        google.protobuf.IntValue retention_25 = 2;
        google.protobuf.IntValue retention_26 = 2;
        google.protobuf.IntValue retention_27 = 2;
        google.protobuf.IntValue retention_28 = 2;
        google.protobuf.IntValue retention_29 = 2;
        google.protobuf.IntValue retention_30 = 2;
        google.protobuf.IntValue install_coun = 2;
"""

result_list = []
for index, line in enumerate(prote_str.strip().split('\n')):
    if line:
        res_line = line.split('=')[0] + '= ' + str(index + 1) + ';' + line.split('=')[1].split(';')[-1]
        result_list.append(res_line)

s = '\n'.join(result_list)
print(s)
