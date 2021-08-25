from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date, timedelta, datetime
import os
import csv


class applovin_calc:
    # _app_list = ['saori_gp', 'dohko_gp', 'aiolos_gp']
    _app_list = ['aiolos_gp']
    _app_package_name_map = {
        'saori_gp': 'art.color.planet.paint.by.number.game.puzzle.free',
        'dohko_gp': 'art.color.planet.oil.paint.canvas.number.free',
        'aiolos_gp': 'art.color.planet.jigsaw.puzzle.online.free',
    }
    _date_start = date(2021, 6, 1)
    _date_end = date(2021, 6, 30)
    _date_step = 6

    def db_conn(self):
        # engine_PROD = create_engine('postgres://gv_developer:AjFtinLDMQ0w7i0f@3.230.194.153:5200/db_redshift_gv')
        # dbsession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_PROD))

        engine_DEV = create_engine(
            'postgres://awsuser:bYPoGonCjqlee5WNj@redshift-cluster-2.cltonxgv2obv.us-east-1.redshift.amazonaws.com:5439/db_redshift_dev')
        dbsession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_DEV))
        return dbsession()

    def get_country_filter(self):
        # sql_statement = """
        #     select
        #         app_name,
        #         country
        #     from (
        #         select app_name,
        #             country,
        #             sum(kch_dnu),
        #             row_number() over (partition by app_name order by sum(kch_dnu) desc) as p
        #         from
        #             mid_poseidon_day_dau_dnu
        #         where
        #             app_name in ('saori_gp', 'aiolos_gp', 'dohko_gp')
        #             and trunc(date) >= '2021-06-01'
        #             and trunc(date) <= '2021-06-30'
        #             and kch_dnu > 0
        #         group by
        #             app_name,
        #             country
        #     ) country_temp
        #     where country_temp.p <= 3;
        #     """
        #
        # rs = self.db_conn().execute(sql_statement)
        # country_map = {}
        # country_list = []
        # for r in rs:
        #     app_name = r[0]
        #     country = r[1]
        #     if app_name not in country_map.keys():
        #         country_map.setdefault(app_name, [])
        #         country_list = []
        #     country_list.append(country)
        #     country_map[app_name] = country_list

        # country_map = {'dohko_gp': ['US', 'PH', 'RU'],
        #                'saori_gp': ['IN', 'BR', 'MX', 'EG', 'PK', 'CO', 'PE', 'AR', 'PH', 'ID', 'TR', 'DZ', 'UZ', 'GT',
        #                             'RU', 'US', 'EC', 'BO', 'TH', 'MY', 'BD', 'HN', 'KZ', 'DO', 'LB', 'CL', 'SA', 'LK',
        #                             'JO'],
        #                'aiolos_gp': ['BR', 'MX', 'IN']}

        country_map = {'aiolos_gp': ['US']}


        return country_map

    # def aggregation_calc(self, country_map, app_name, result_data_map_list):
    #     country_list = country_map.get(app_name)
    #     country_summary = {}
    #     for country in country_list:
    #         sum_List = []
    #         for i in range(len(result_data_map_list)):
    #             sum_List.append(result_data_map_list[i][country])
    #         country_summary[country] = self.map_sum(sum_List)
    #     return country_summary

    # def calc(self, map1, map2):
    #     for k, v in map2.items():
    #         if k in map1.keys():
    #             map1[k] += v
    #         else:
    #             map1[k] = v
    #     return map1

    # def map_sum(self, list):
    #     if len(list) == 1:
    #         return list[0]
    #     else:
    #         return self.calc(list[0], self.map_sum(list[1:]))

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
        result_date_summary = {}
        rowset_list = []
        for app_name in self._app_list:
            sql_statement = """
                                with user_install_info as (
                                    select 
                                        info.country as country,
                                        info.muid,
                                        info.ins_date
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
                                    count(distinct info.muid) as muid_count,
                                    sum(muid_count) over (partition by country order by comp_type rows between current row and unbounded following) as sum_count
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
                                    type.comp_type
                                order by
                                    info.country, 
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
            print(sql_statement)
            db_session = self.db_conn()
            rowset = db_session.execute(sql_statement)
            rowset_list.append(rowset)
        self.get_result_csv(rowset_list, app_name)

    def get_result_csv(self, rowset_list, app_name):
        dnu_map = self.get_sum_dnu_map(app_name)
        filepath = f'/Users/long.tian/Desktop/Applovin_res/test.csv'
        with open(filepath, 'w') as file:
            file.write(','.join(['trigger_type', 'app_name', 'country', 'sum_dnu', 'eu', 'persent']))
            file.write('\n')
            for rs in rowset_list:
                for r in rs:
                    country = r[0]
                    trigger_type = r[1]
                    trigger_num = r[3]
                    dnu_sum = dnu_map.get(country)
                    persent = 1.0 * trigger_num / dnu_sum
                    data = ','.join([str(trigger_type), app_name, country, str(dnu_sum), str(trigger_num), str(persent)])
                    file.write(data)
                    file.write('\n')






if __name__ == '__main__':
    app = applovin_calc()
    res = app.interstitial_and_rewardedvideo_calc()
    # print(res)
