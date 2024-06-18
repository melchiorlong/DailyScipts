from ProvinceCityPinyinConvert import ProvinceCityPinyinConvert
from GetGasolinePrice import GetGasolinePrice

# arg_str = '北京'
# region = ProvinceCityPinyinConvert(arg_str).get_region_pinyin()
# res = GetGasolinePrice(region).get_price()
# print(res)

res = {
    '95': '8.36',
    '98': '9.86',
    'update_time': '2024-06-18',
    'tips': '目前预计上调110元/吨(0.08元/升-0.10元/升)，大家相互转告开始上涨',
    'next_adjust': '下次油价6月27日24时调整'
}
str1 = '95号汽油：' + str(res['95']) + '元每升,'
str2 = '98号汽油：' + str(res['98']) + '元每升。'
str3 = '更新日期：' + str(res['update_time']) + '。'
str4 = str(res['next_adjust']) + '，'
str5 = str(res['tips']).split("，")[0] + '。'

res_str = str1 + str2 + str3 + str4 + str5

print(res_str)
