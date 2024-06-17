from ProvinceCityPinyinConvert import ProvinceCityPinyinConvert
from GetGasolinePrice import GetGasolinePrice

region = ProvinceCityPinyinConvert('北京').get_region_pinyin()
res = GetGasolinePrice(region).get_price()
print(res)