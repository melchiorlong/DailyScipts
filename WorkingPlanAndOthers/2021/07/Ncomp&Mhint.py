from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date, timedelta, datetime
import os
import csv
import sys  # 导入sys模块


class applovin_complete_and_hint_calc:
    # _app_list = ['saori_gp', 'dohko_gp', 'aiolos_gp']
    _app_list = ['aiolos_gp']
    _date_start = date(2021, 6, 1)
    _date_end = date(2021, 6, 30)
    _date_step = 6
    sys.setrecursionlimit(3000)  # 将默认的递归深度修改为3000

    def db_conn(self):
        # engine_PROD = create_engine('postgres://gv_developer:AjFtinLDMQ0w7i0f@3.230.194.153:5200/db_redshift_gv')
        # dbsession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_PROD))

        engine_DEV = create_engine(
            'postgres://awsuser:bYPoGonCjqlee5WNj@redshift-cluster-2.cltonxgv2obv.us-east-1.redshift.amazonaws.com:5439/db_redshift_dev')
        dbsession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_DEV))
        return dbsession()

    def get_country_filter(self):
        # country_map = {'dohko_gp': ['US', 'PH', 'RU'],
        #                'saori_gp': ['IN', 'BR', 'MX', 'EG', 'PK', 'CO', 'PE', 'AR', 'PH', 'ID', 'TR', 'DZ', 'UZ', 'GT',
        #                             'RU', 'US', 'EC', 'BO', 'TH', 'MY', 'BD', 'HN', 'KZ', 'DO', 'LB', 'CL', 'SA', 'LK',
        #                             'JO'],
        #                'aiolos_gp': ['BR', 'MX', 'IN']}

        country_map = {'aiolos_gp': ['BR', 'MX', 'IN']}

        return country_map

    def get_sum_dnu_map(self, app_name):
        sql_statement = """
            select 
                info.country,
                count(distinct muid) as sum_dnu
            from 
                temp_applovin_kch_install info
            where 1 = 1
                and info.app_name = '{app_name}'
                group by 
                    info.country;
        """.format(
            app_name=app_name,
        )
        db_session = self.db_conn()
        rs = db_session.execute(sql_statement)
        country_map = {}
        for r in rs:
            country = r[0]
            sum_dnu = r[1]
            country_map.setdefault(country)
            country_map[country] = sum_dnu
        return country_map

    def interstitial_and_rewardedvideo_calc(self):

        country_map = self.get_country_filter()
        rowset_list = []
        for app_name in self._app_list:
            sql_statement = """
                with user_install_info as (
                    select 
                        info.country as country,
                        info.muid,
                        info.ins_date,
                        info.app_name
                    from 
                        temp_applovin_kch_install info
                    where 1 = 1
                        and info.app_name = '{app_name_iter}'
                        and trunc(info.ins_date) >= '{date_start}'
                        and trunc(info.ins_date) <= '{date_end}'
                        {country_filter}
                ),
                type_temp as (
                    select 
                        info.muid,
                        sum(hint_count) as hint_type,
                        sum(complete_count) as comp_type
                    from 
                        temp_applovin_{app_table_iter}_log log
                        inner join user_install_info info 
                        on info.muid = log.muid
                    where 1 = 1
                        and log.action_date <= trunc(dateadd(day, {date_step}, info.ins_date))
                    group by 
                        info.muid
                )
                select 
                    info.country,
                    type.comp_type,
                    type.hint_type,
                    count(distinct info.muid) as muid_count,
                    info.app_name
                from 
                    temp_applovin_{app_table_iter}_log log
                inner join
                    user_install_info info
                    on info.muid = log.muid
                inner join 
                type_temp type
                    on log.muid = type.muid
                group by 
                    info.country,
                    type.comp_type,
                    type.hint_type,
                    info.app_name
                order by
                    info.country, 
                    type.hint_type,
                    type.comp_type;
            """.format(
                date_start=self._date_start,
                date_end=self._date_end,
                app_name_iter=app_name,
                app_table_iter=app_name[:-3],
                date_step=self._date_step,
                country_filter="and info.country in ({countries})".format(
                    countries="'" + "','".join(country_map.get(app_name)) + "'"
                ),
            )
            # print(sql_statement)
            db_session = self.db_conn()
            rowset = db_session.execute(sql_statement)
            rowset_list.append(rowset)
            # self.get_result_csv(rowset_list)

            # sum_rowset = self.rowset_sum(rowset)
            # print(sum_rowset)

            res_map_temp = {}
            data_list = []
            for r in rowset:
                data_map_temp = {}
                country = r[0]
                complete_type = r[1]
                hint_type = r[2]
                muid_count = r[3]
                app_name = r[4]

                res_map_temp.setdefault(country, [])
                data_map_temp.setdefault((complete_type, hint_type), muid_count)
                data_list.append(data_map_temp)
                res_map_temp[country] = (data_list)

            result = self.rowset_sum(res_map_temp)

            print(result)

            # todo 继续包装
            # self.get_result_csv(result)


    # def get_result_csv(self, rowset_list):
    #     dnu_map = {}
    #     for app_name in self._app_list:
    #         dnu_map[app_name] = self.get_sum_dnu_map(app_name)
    #
    #     filename = self.__class__.__name__
    #     filepath = f'/Users/long.tian/Desktop/Applovin_res/{filename}.csv'
    #     with open(filepath, 'w') as file:
    #         file.write(','.join(['complete(m)', 'hint(n)', 'app_name', 'country', 'dnu', 'eu', 'percentage']))
    #         file.write('\n')
    #         for rs in rowset_list:
    #             for r in rs:
    #                 country = r[0]
    #                 complete_type = r[1]
    #                 hint_type = r[2]
    #                 muid_count = r[3]
    #                 app_name = r[4]
    #                 dnu_sum = dnu_map[app_name].get(country)
    #                 persent = 1.0 * sum_count / dnu_sum
    #                 data = ','.join([str(complete_type), str(hint_type), app_name, country, str(dnu_sum), str(sum_count), str(persent)])
    #                 file.write(data)
    #                 file.write('\n')

    def calc(self, map1, map2):
        for k, v in map2.items():
            for key, value in map1.items():
                map1[key] += v
        return map1

    def map_sum(self, list):
        if len(list) == 1:
            return list[0]
        else:
            return self.calc(list[0], self.map_sum(list[1:]))

    def get_key_list(self, list):
        key_list = []
        for data_map in list:
            for k, v in data_map.items():
                key_list.append(k)
        return key_list

    def rowset_sum(self, rowset):
        res = {}
        res_map = {}
        for country, data_map in rowset.items():
            key_list = self.get_key_list(data_map)
            for key in key_list:
                map_temp = []
                for i in data_map:
                    for k, v in i.items():
                        if k[0] >= key[0] and k[1] >= key[1]:
                            map_temp.append({k: v})
                map_res = self.map_sum(map_temp)
                res.update(map_res)
            res_map.setdefault(country, {})
            res_map[country] = res

        return res_map


if __name__ == '__main__':
    start = datetime.now()
    print('开始时间' + start.strftime('%Y-%m-%d %H:%M:%S'))

    app = applovin_complete_and_hint_calc()
    res = app.interstitial_and_rewardedvideo_calc()

    end = datetime.now()
    duration = end - start
    print('结束时间' + end.strftime('%Y-%m-%d %H:%M:%S') + ', 用时' + str(duration.seconds) + '秒。')
