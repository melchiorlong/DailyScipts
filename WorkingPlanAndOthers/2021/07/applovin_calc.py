from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date, timedelta
import os


class applovin_calc:
    _app_list = ['saori_gp', 'dohko_gp', 'aiolos_gp']
    _app_package_name_map = {
        'saori_gp': 'art.color.planet.paint.by.number.game.puzzle.free',
        'dohko_gp': 'art.color.planet.oil.paint.canvas.number.free',
        'aiolos_gp': 'art.color.planet.jigsaw.puzzle.online.free',
    }
    _date_start = date(2021, 6, 1)
    _date_end = date(2021, 6, 30)
    _date_step = 7

    def db_conn(self):
        # engine_PROD = create_engine('postgres://gv_developer:AjFtinLDMQ0w7i0f@3.230.194.153:5200/db_redshift_gv')
        # dbsession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_PROD))

        engine_DEV = create_engine(
            'postgres://awsuser:bYPoGonCjqlee5WNj@redshift-cluster-2.cltonxgv2obv.us-east-1.redshift.amazonaws.com:5439/db_redshift_dev')
        dbsession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_DEV))
        return dbsession()

    def result_mkdir(self, country_map):
        for item in self._app_list:
            country_list = country_map.get(item)
            for country in country_list:
                os.mkdir(r'/Users/long.tian/Downloads/applovin_data/rewardedvideo/' + item + '/' + country)

    def get_country_filter(self):
        sql_statement = """
            select 
                app_name, 
                country
            from (
                select app_name,
                    country,
                    sum(kch_dnu),
                    row_number() over (partition by app_name order by sum(kch_dnu) desc) as p
                from 
                    mid_poseidon_day_dau_dnu
                where 
                    app_name in ('saori_gp', 'aiolos_gp', 'dohko_gp')
                    and trunc(date) >= '2021-06-01'
                    and trunc(date) <= '2021-06-30'
                    and kch_dnu > 0
                group by 
                    app_name, 
                    country
            ) country_temp
            where country_temp.p <= 3;
            """

        rs = self.db_conn().execute(sql_statement)
        country_map = {}
        country_list = []
        for r in rs:
            app_name = r[0]
            country = r[1]
            if app_name not in country_map.keys():
                country_map.setdefault(app_name, [])
                country_list = []
            country_list.append(country)
            country_map[app_name] = country_list
        print(country_map)
        return country_map

    def aggregation_calc(self, country_map, app_name, result_data_map_list):
        country_list = country_map.get(app_name)
        country_summary = {}
        for country in country_list:
            sum_List = []
            for i in range(len(result_data_map_list)):
                sum_List.append(result_data_map_list[i][country])
            country_summary[country] = self.map_sum(sum_List)
        return country_summary

    def calc(self, map1, map2):
        for k, v in map1.items():
            if k in map2.keys():
                map2[k] += v
            else:
                map2[k] = v
        return map2

    def map_sum(self, list):
        if len(list) == 1:
            return list[0]
        else:
            return self.calc(list[0], self.map_sum(list[1:]))

    def interstitial_and_rewardedvideo_calc(self):
        # todo country filter
        # todo date iterator
        # todo app_name iterator
        # todo table name within app name iterator

        country_map = self.get_country_filter()
        res = {}
        for app_name in self._app_list:
            print(app_name)
            result_date_summary = {}
            result_data_map_list = []
            result_date_summary[app_name] = result_data_map_list
            day_str = ''
            for i in range((self._date_end - self._date_start).days + 1):
                day = self._date_start + timedelta(days=i)
                day_str = day.strftime('%Y-%m-%d')
                print(day_str)
                sql_statement = """
                    with temp_e as (
                        select dim.kch_country,
                            dim.muid                                                                            as trigger_muid,
                            sum(case when log.ad_format in ('interstitial', 'rewardedvideo') then 1 else 0 end) as trigger_type
                        from kch_{app_name_iter}_install_info info
                        inner join
                            muid_dimension dim
                        on 
                            info.kochava_device_id = dim.kch_id
                            and trunc(info.date_occurred) = '{date_iter}'
                            {country_filter}
                        left join
                            temp_applovin_poseidon_log log
                        on 
                            dim.muid = log.muid
                            and trunc(log.action_time) >= '{date_iter}'
                            and trunc(log.action_time) <= trunc(dateadd(day, 7, '{date_iter}'))
                            {app_package_name_filter}
                        group by 
                            dim.kch_country,
                            dim.muid
                        order by trigger_type
                    ),
                    temp as (
                        select kch_country,
                            temp_e.trigger_type,
                            count(distinct temp_e.trigger_muid) as trigger_num
                        from temp_e
                        group by 
                            temp_e.kch_country, 
                            temp_e.trigger_type
                    )
                    select temp.kch_country,
                        temp.trigger_type,
                        temp.trigger_num
                    from temp
                    order by 
                        temp.kch_country, 
                        temp.trigger_type;
                """.format(
                    app_name_iter=app_name,
                    country_filter="and dim.kch_country in ({countries})".format(
                        countries="'" + "','".join(country_map.get(app_name)) + "'"
                    ),
                    date_iter=day_str,
                    app_package_name_filter="and log.app_package_name = '{package_name}'".format(
                        package_name=self._app_package_name_map.get(app_name)
                    )
                )
                print(sql_statement)
                db_session = self.db_conn()
                rs = db_session.execute(sql_statement)
                result_map = {}
                result_data_map = {}
                result_data_map_list = []
                for r in rs:
                    country = r[0]
                    trigger_type = r[1]
                    trigger_num = r[2]
                    if country not in result_map.keys():
                        result_map.setdefault(country, {})
                        result_data_map = {}
                    result_data_map[trigger_type] = trigger_num
                    result_map[country] = result_data_map
                result_data_map_list.append(result_map)

            result = self.aggregation_calc(country_map, app_name, result_data_map_list)

            result_date_summary[app_name].append(result)
            res = {day_str: result_date_summary}

        return res


if __name__ == '__main__':
    app = applovin_calc()
    app.interstitial_and_rewardedvideo_calc()
