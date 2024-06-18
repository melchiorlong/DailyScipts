from ProvinceCityPinyinConvert import ProvinceCityPinyinConvert
from GetGasolinePrice import GetGasolinePrice
import sys
import json

arg_str = sys.argv[1]
if '~' or '～' in arg_str:
    def create_item(title, subtitle, icon, arg):
        item = {
            'title': title,
            'subtitle': subtitle,
            'icon': icon,
            'arg': arg
        }
        return item


    def task_run():
        region = ProvinceCityPinyinConvert(arg_str).get_region_pinyin()
        res = GetGasolinePrice(region).get_price()
        str1 = '95号汽油：' + str(res['95']) + '元每升,'
        str2 = '98号汽油：' + str(res['98']) + '元每升。'
        str3 = '更新日期：' + str(res['update_time']) + '。'
        str4 = str(res['next_adjust']) + '，'
        str5 = str(res['tips']).split("，")[0] + '。'
        res_str1 = str1 + str2
        res_str2 = str3 + str4 + str5

        items = [create_item(
            str(res_str1),
            res_str2,
            {},
            str(res_str1),
        )]
        result = {'items': items}
        print(json.dumps(result))
