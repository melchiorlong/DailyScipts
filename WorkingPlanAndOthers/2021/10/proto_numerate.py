prote_str = """
            google.protobuf.BoolValue day0_cost_exclude_yesterday = 117;
            google.protobuf.FloatValue day0_cost_ignore_fb = 118;
            google.protobuf.FloatValue day0_cost = 53;  // ddd
            google.protobuf.FloatValue day0_ads_rev = 54;
            google.protobuf.FloatValue day0_iap_rev = 55;
            google.protobuf.BoolValue day0_rev_ge_3 = 56;
            google.protobuf.FloatValue day1_cost = 57;
            google.protobuf.FloatValue day1_ads_rev = 58;
            google.protobuf.FloatValue day1_iap_rev = 59;
            google.protobuf.BoolValue day1_rev_ge_3 = 60;
            google.protobuf.FloatValue day2_cost = 61;
            google.protobuf.FloatValue day2_ads_rev = 62;
            google.protobuf.FloatValue day2_iap_rev = 63;
            google.protobuf.BoolValue day2_rev_ge_3 = 64;
            google.protobuf.FloatValue day3_cost = 65;
            google.protobuf.FloatValue day3_ads_rev = 66;
            google.protobuf.FloatValue day3_iap_rev = 67;
            google.protobuf.BoolValue day3_rev_ge_3 = 68;
            google.protobuf.FloatValue day7_cost = 69;
            google.protobuf.FloatValue day7_ads_rev = 70;
            google.protobuf.FloatValue day7_iap_rev = 71;
            google.protobuf.BoolValue day7_rev_ge_3 = 72;
            google.protobuf.FloatValue day14_cost = 73;
            google.protobuf.FloatValue day14_ads_rev = 74;
            google.protobuf.FloatValue day14_iap_rev = 75;
            google.protobuf.BoolValue day14_rev_ge_3 = 76;
            google.protobuf.FloatValue day30_cost = 77;
            google.protobuf.FloatValue day30_ads_rev = 78;
            google.protobuf.FloatValue day30_iap_rev = 79;
            google.protobuf.BoolValue day30_rev_ge_3 = 80;
"""

result_list = []
for index, line in enumerate(prote_str.strip().split('\n')):
    if line:
        res_line = line.split('=')[0] + '= ' + str(index + 1) + ';' + line.split('=')[1].split(';')[-1]
        result_list.append(res_line)

s = '\n'.join(result_list)
print(s)
