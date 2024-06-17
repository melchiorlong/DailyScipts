from fuzzywuzzy import process
from ProvinceCityDicts import ProvinceCityDicts
from pypinyin import lazy_pinyin, Style


class ProvinceCityPinyinConvert:

    def __init__(self, city_name):
        self.city_name = city_name

    def get_major_city_list(self):
        major_cities = []
        for province_info_dict in ProvinceCityDicts.PROVINCE_LIST:
            province_name = province_info_dict["name"]
            major_cities.append(province_name)
        return major_cities

    def get_second_major_city_list(self):
        secondary_cities = []
        for province_id, city_info_list in ProvinceCityDicts.CITY_MAP.items():
            for city_info in city_info_list:
                city_name = city_info["name"]
                secondary_cities.append(city_name)
        return secondary_cities

    def find_closest_city(self, query, city_list):
        matches = process.extract(query, city_list, limit=1)
        return matches[0][0]

    def get_city_pinyin(self, matches_city):
        city_idx = lazy_pinyin(matches_city, style=Style.FIRST_LETTER)[0].upper()
        city_pinyin = ''
        for idx_list in ProvinceCityDicts.PROVINCE_CITY_MAP['cityList']:
            if idx_list['idx'] == city_idx:
                for city in idx_list['cities']:
                    if city['name'] == matches_city:
                        city_pinyin = city['pinyin']
        return city_pinyin

    def get_province_pinyin(self, matches_city):
        province_pinyin = ''
        for province_id, city_info_list in ProvinceCityDicts.CITY_MAP.items():
            for city_info in city_info_list:
                if city_info['name'] == matches_city:
                    for province_info in ProvinceCityDicts.PROVINCE_LIST:
                        if city_info['province'] == province_info['name']:
                            province_pinyin = province_info['pinyin']
        return province_pinyin

    def get_region_pinyin(self):
        major_cities = self.get_major_city_list()
        secondary_cities = self.get_second_major_city_list()
        all_cities = major_cities + secondary_cities
        matches_city = self.find_closest_city(self.city_name, all_cities)
        city_pinyin = self.get_city_pinyin(matches_city)
        province_pinyin = self.get_province_pinyin(matches_city)
        region_pinyin = ''
        if matches_city in major_cities:
            region_pinyin = city_pinyin
        else:
            region_pinyin = province_pinyin + '/' + city_pinyin
        return region_pinyin
