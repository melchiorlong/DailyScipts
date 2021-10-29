
path = r'/Users/long.tian/Downloads/data.csv'
predict_data = {}
with open(path, 'r') as f:
    lines = f.readlines()
    header = lines[0].strip().split(',')

    campaign_id_index = header.index('campaign_id')
    ins_date_index = header.index('date')
    country_index = header.index('country')
    spend_index = header.index('spend')
    roi30_index = header.index('all_predict')

    for _line in lines[1:]:
        line = _line.strip().split(',')
        campaign_id = line[campaign_id_index]
        ins_date = line[ins_date_index]
        country = line[country_index]
        spend = float(line[spend_index] if line[spend_index] else 0)
        roi30 = float(line[roi30_index] if line[roi30_index] else 0)
        predict_data.setdefault(campaign_id, {})
        predict_data[campaign_id].setdefault(ins_date, {})
        predict_data[campaign_id][ins_date].setdefault(country, {})
        predict_data[campaign_id][ins_date][country] = {
            'spend': spend,
            'rev_30': spend * roi30
        }

def get_predict_roi30(campaing_id, date, country):
    return predict_data[campaing_id][date][country]


d = get_predict_roi30('12088097929', '2021-10-01', 'JP')
print(d)