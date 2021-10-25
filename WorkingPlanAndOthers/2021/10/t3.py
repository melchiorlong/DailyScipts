import datetime

l1 = \
    {'campaign_id': '12571866870', 'campaign_name': 'gv_jimmy_saori_ip_us_0318#fans4', 'media_source': 'Google',
     'country_list': ['US'],
     'ret1_info_list': [{'date': datetime.date(2021, 10, 1), 'num': None},
                        {'date': datetime.date(2021, 10, 2), 'num': None},
                        {'date': '2021-10-01', 'num': None},
                        {'date': '2021-10-02', 'num': None}],
     'ret7_info_list': [{'date': datetime.date(2021, 10, 1), 'num': None},
                        {'date': datetime.date(2021, 10, 2), 'num': None}, {'date': '2021-10-01', 'num': None},
                        {'date': '2021-10-02', 'num': None}], 'roi0_info_list': [
        {'date': datetime.date(2021, 10, 1), 'numerator': 20.6608072335835, 'denominator': 1274.398757},
        {'date': datetime.date(2021, 10, 2), 'numerator': 25.6494595343869, 'denominator': 1276.236651},
        {'date': '2021-10-01', 'numerator': None, 'denominator': None},
        {'date': '2021-10-02', 'numerator': None, 'denominator': None}], 'roi7_info_list': [
        {'date': datetime.date(2021, 10, 1), 'numerator': 47.7097780104139, 'denominator': 1274.398757},
        {'date': datetime.date(2021, 10, 2), 'numerator': 56.0819663301863, 'denominator': 1276.236651},
        {'date': '2021-10-01', 'numerator': None, 'denominator': None},
        {'date': '2021-10-02', 'numerator': None, 'denominator': None}], 'roi30_info_list': [
        {'date': datetime.date(2021, 10, 1), 'numerator': 54.8078212829742, 'denominator': 1274.398757},
        {'date': datetime.date(2021, 10, 2), 'numerator': 61.7264759740968, 'denominator': 1276.236651},
        {'date': '2021-10-01', 'numerator': None, 'denominator': None},
        {'date': '2021-10-02', 'numerator': None, 'denominator': None}],
     'cost_info_list': [{'date': datetime.date(2021, 10, 1), 'num': 1274.398757},
                        {'date': datetime.date(2021, 10, 2), 'num': 1276.236651}, {'date': '2021-10-01', 'num': None},
                        {'date': '2021-10-02', 'num': None}],
     'kov_dnu_info_list': [{'date': datetime.date(2021, 10, 1), 'num': None},
                           {'date': datetime.date(2021, 10, 2), 'num': None}, {'date': '2021-10-01', 'num': None},
                           {'date': '2021-10-02', 'num': None}],
     'dnu_info_list': [{'date': datetime.date(2021, 10, 1), 'num': None},
                       {'date': datetime.date(2021, 10, 2), 'num': None}, {'date': '2021-10-01', 'num': 72},
                       {'date': '2021-10-02', 'num': 71}],
     'kov_cpi_info_list': [{'date': datetime.date(2021, 10, 1), 'numerator': 1274.398757, 'denominator': None},
                           {'date': datetime.date(2021, 10, 2), 'numerator': 1276.236651, 'denominator': None},
                           {'date': '2021-10-01', 'numerator': None, 'denominator': None},
                           {'date': '2021-10-02', 'numerator': None, 'denominator': None}],
     'cpi_info_list': [{'date': datetime.date(2021, 10, 1), 'numerator': 1274.398757, 'denominator': None},
                       {'date': datetime.date(2021, 10, 2), 'numerator': 1276.236651, 'denominator': None},
                       {'date': '2021-10-01', 'numerator': None, 'denominator': 72},
                       {'date': '2021-10-02', 'numerator': None, 'denominator': 71}],
     'ctr_info_list': [{'date': datetime.date(2021, 10, 1), 'numerator': 1936, 'denominator': 86103},
                       {'date': datetime.date(2021, 10, 2), 'numerator': 1869, 'denominator': 87275},
                       {'date': '2021-10-01', 'numerator': None, 'denominator': None},
                       {'date': '2021-10-02', 'numerator': None, 'denominator': None}],
     'cvr_info_list': [{'date': datetime.date(2021, 10, 1), 'numerator': 221, 'denominator': 221},
                       {'date': datetime.date(2021, 10, 2), 'numerator': 224, 'denominator': 224},
                       {'date': '2021-10-01', 'numerator': None, 'denominator': None},
                       {'date': '2021-10-02', 'numerator': None, 'denominator': None}],
     'cpm_info_list': [{'date': datetime.date(2021, 10, 1), 'numerator': 1274.398757, 'denominator': 86103},
                       {'date': datetime.date(2021, 10, 2), 'numerator': 1276.236651, 'denominator': 87275},
                       {'date': '2021-10-01', 'numerator': None, 'denominator': None},
                       {'date': '2021-10-02', 'numerator': None, 'denominator': None}]}

t1 = datetime.date(2021, 10, 1)
# t1 = datetime.datetime(2012, 11, 19, 0, 0)
print(t1)

print(t1.strftime('%Y-%m-%d'))
