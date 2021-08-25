from datetime import datetime, timedelta


def check_and_add_single_country_analysis_date(date_start, date_end, data_list, default_dict=None):
    # 确保date_start至date_end之间的date都出现过
    date_start = datetime.strptime(date_start, '%Y-%m-%d')
    date_end = datetime.strptime(date_end, '%Y-%m-%d')
    date_set = set([d['date'] for d in data_list])
    while date_start <= date_end:
        date_str = date_start.strftime('%Y-%m-%d')
        if date_str not in date_set:
            date_data = {'date': date_str}
            if default_dict:
                date_data.update(default_dict)
            data_list.append(date_data)
        date_start += timedelta(days=1)
    return sorted(data_list, key=lambda d: d['date'])


def check_and_add_monetization_analysis_date(date_start, date_end, data_list, summary_key, default_dict=None):
    # 确保date_start至date_end之间的date都出现过
    for i in data_list:
        res = []
        for ele in check_and_add_single_country_analysis_date(date_start, date_end, i[summary_key], default_dict):
            res.append(ele)
        i[summary_key] = res
    return data_list


if __name__ == '__main__':
    dnu_dau_datalist = [
        {
            "date": '2021-06-01',
            "kch_dau": 1,
            "kch_dnu": 1,
            "flurry_dau": 1,
            "flurry_dnu": 1,
        }, {
            "date": '2021-06-02',
            "kch_dau": 2,
            "kch_dnu": 2,
            "flurry_dau": 2,
            "flurry_dnu": 2,
        }, {
            "date": '2021-06-03',
            "kch_dau": 3,
            "kch_dnu": 3,
            "flurry_dau": 3,
            "flurry_dnu": 3,
        },
    ]

    dnu_dau_default_dict = {"kch_dau": 0,
                            "kch_dnu": 0,
                            "flurry_dau": 0,
                            "flurry_dnu": 0}

    daily_rev_datalist = [
        {
            "date": "2021-06-01",
            "revenue_detail": {
                "groupname1": 1,
                "groupname2": 1,
            },
        },
        {
            "date": "2021-06-02",
            "revenue_detail": {
                "groupname1": 2,
                "groupname2": 2,
            },
        },
        {
            "date": "2021-06-03",
            "revenue_detail": {
                "groupname1": 3,
                "groupname2": 3,
            },
        },
    ]

    daily_rev_dd = {
        "revenue_detail": {
            "groupname1": 0,
            "groupname2": 0,
        },
    }

    arpdau_datalist = [
        {
            'placement': '1',
            'arpdau_summary': [
                {
                    "date": "2021-06-01",
                    "ads_revenue": 11,
                    "dau": 11,
                },
                {
                    "date": "2021-06-02",
                    "ads_revenue": 12,
                    "dau": 12,
                },
                {
                    "date": "2021-06-03",
                    "ads_revenue": 13,
                    "dau": 13,
                },
            ]
        },
        {
            'placement': '2',
            'arpdau_summary': [
                {
                    "date": "2021-06-01",
                    "ads_revenue": 21,
                    "dau": 21,
                },
                {
                    "date": "2021-06-02",
                    "ads_revenue": 22,
                    "dau": 22,
                },
            ]
        },
    ]

    arpdau_dd = {
        "ads_revenue": 0,
        "dau": 0,
    }

    impr_data = [{'placement': 'tora',
                  'daily_summary': [{'date': '2021-06-23', 'impr': 10534, 'sd': 9683},
                                    {'date': '2021-06-24', 'impr': 10100, 'sd': 9410}]},
                 {'placement': 'hebi',
                  'daily_summary': [{'date': '2021-06-23', 'impr': 510076, 'sd': 470539},
                                    {'date': '2021-06-24', 'impr': 465653, 'sd': 431963}]},
                 {'placement': 'tatsu',
                  'daily_summary': [{'date': '2021-06-23', 'impr': 21801, 'sd': 21436},
                                    {'date': '2021-06-24', 'impr': 20876, 'sd': 20916}]}]

# result1 = check_and_add_single_country_analysis_date(
#     '2021-06-01',
#     '2021-06-05',
#     daily_rev_datalist,
#     daily_rev_dd
# )
#
# result2 = check_and_add_monetization_analysis_date(
#     '2021-06-01',
#     '2021-06-05',
#     arpdau_datalist,
#     arpdau_dd
# )


result3 = check_and_add_monetization_analysis_date(
    '2021-06-23',
    '2021-06-27',
    impr_data,
    'daily_summary',
    {"impr": 0, "sd": 0}
)

print(result3)

a = [{'date': '2021-06-01', 'kch_dau': 1, 'kch_dnu': 1, 'flurry_dau': 1, 'flurry_dnu': 1},
     {'date': '2021-06-02', 'kch_dau': 2, 'kch_dnu': 2, 'flurry_dau': 2, 'flurry_dnu': 2},
     {'date': '2021-06-03', 'kch_dau': 3, 'kch_dnu': 3, 'flurry_dau': 3, 'flurry_dnu': 3},
     {'date': '2021-06-04', 'kch_dau': 0, 'kch_dnu': 0, 'flurry_dau': 0, 'flurry_dnu': 0},
     {'date': '2021-06-05', 'kch_dau': 0, 'kch_dnu': 0, 'flurry_dau': 0, 'flurry_dnu': 0}]

b = [{'date': '2021-06-01', 'revenue_detail': {'groupname1': 1, 'groupname2': 1}},
     {'date': '2021-06-02', 'revenue_detail': {'groupname1': 2, 'groupname2': 2}},
     {'date': '2021-06-03', 'revenue_detail': {'groupname1': 3, 'groupname2': 3}},
     {'date': '2021-06-04', 'revenue_detail': {'groupname1': 0, 'groupname2': 0}},
     {'date': '2021-06-05', 'revenue_detail': {'groupname1': 0, 'groupname2': 0}}]

c = [{'placement': '1', 'arpdau_summary': [{'date': '2021-06-01', 'ads_revenue': 11, 'dau': 11},
                                           {'date': '2021-06-02', 'ads_revenue': 12, 'dau': 12},
                                           {'date': '2021-06-03', 'ads_revenue': 13, 'dau': 13},
                                           {'date': '2021-06-04', 'ads_revenue': 0, 'dau': 0},
                                           {'date': '2021-06-05', 'ads_revenue': 0, 'dau': 0}]},
     {'placement': '2', 'arpdau_summary': [{'date': '2021-06-01', 'ads_revenue': 21, 'dau': 21},
                                           {'date': '2021-06-02', 'ads_revenue': 22, 'dau': 22},
                                           {'date': '2021-06-03', 'ads_revenue': 0, 'dau': 0},
                                           {'date': '2021-06-04', 'ads_revenue': 0, 'dau': 0},
                                           {'date': '2021-06-05', 'ads_revenue': 0, 'dau': 0}]}]

[{'date': '2021-06-23', 'revenue_detail': {'tora': 167.1970977783203, 'hebi': 116.64855194091797}},
 {'date': '2021-06-24', 'revenue_detail': {'hebi': 112.78865814208984, 'tora': 145.97203063964844}},
 {'date': '2021-06-25', 'groupname1': 0, 'groupname2': 0}, {'date': '2021-06-26', 'groupname1': 0, 'groupname2': 0},
 {'date': '2021-06-27', 'groupname1': 0, 'groupname2': 0}, {'date': '2021-06-28', 'groupname1': 0, 'groupname2': 0}]
