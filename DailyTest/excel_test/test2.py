import pandas as pd


city_name = ''
data = pd.read_excel('/Users/miaolin/Desktop/样例指标.xlsx')
index_list = data.columns[1:]
city_list = data['城市'].tolist()
city_index = city_list.index(city_name)
city_result = data.loc[city_index]
result1, result2 = [], []

group_set = data['分组'].toSet()
res_greater_dict = {}
res_less_dict = {}


for group in group_set:
    for i in index_list:
        if group == data.columns[1]:
            result_list = data[i].tolist()
            result_list = list(map(float, result_list))

            if float(city_result[i]) >= sum(result_list) / len(result_list):
                result1.append(i)
                res_greater_dict[group] = result1
            elif float(city_result[i]) <= sum(result_list) / len(result_list):
                result2.append(i)
                res_less_dict[group] = result1
            else:
                pass




