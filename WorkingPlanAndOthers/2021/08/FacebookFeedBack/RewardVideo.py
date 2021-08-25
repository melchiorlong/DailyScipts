from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date, timedelta, datetime
import os
import csv


class applovin_reward_video_calc:
    # _app_list = ['saori_gp', 'dohko_gp', 'aiolos_gp','saori_ip', 'dohko_ip', 'aiolos_ip','saga_gp']
    _app_list = ['aiolos_gp', 'dohko_gp']
    _date_start = date(2021, 7, 20)
    _date_end = date(2021, 8, 19)
    _date_step = 1

    def db_conn(self):
        # engine_PROD = create_engine('postgres://gv_developer:AjFtinLDMQ0w7i0f@3.230.194.153:5200/db_redshift_gv')
        # dbsession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_PROD))

        engine_DEV = create_engine(
            'postgres://awsuser:bYPoGonCjqlee5WNj@redshift-cluster-2.cltonxgv2obv.us-east-1.redshift.amazonaws.com:5439/db_redshift_dev')
        dbsession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_DEV))
        return dbsession()

    def get_country_filter(self):
        country_map = {'dohko_gp': ['US', 'PH', 'RU'],
                       'saori_gp': ['IN', 'BR', 'MX', 'EG', 'PK', 'CO', 'PE', 'AR', 'PH', 'ID', 'TR', 'DZ', 'UZ', 'GT',
                                    'RU', 'US', 'EC', 'BO', 'TH', 'MY', 'BD', 'HN', 'KZ', 'DO', 'LB', 'CL', 'SA', 'LK',
                                    'JO'],
                       'aiolos_gp': ['BR', 'MX', 'IN'],
                       'aiolos_ip': [''],
                       'saori_ip': [''],
                       'dohko_ip': [''],
                       'saga_gp': [''],
                       }

        # country_map = {'aiolos_gp': ['BR', 'AR']}

        return country_map

    def get_sum_dnu_map(self, app_name):
        sql_statement = """
            select 
                info.country,
                count(distinct muid) as sum_dnu
            from 
                temp_install_info info
            where 1 = 1
                and info.app_name = '{app_name}'
                group by 
                    info.country;
        """.format(
            app_name=app_name,
        )
        db_session = self.db_conn()

        # rs = db_session.execute(sql_statement)
        print(sql_statement)

        country_map = {}
        for r in rs:
            country = r[0]
            sum_dnu = r[1]
            country_map.setdefault(country)
            country_map[country] = sum_dnu
        return country_map

    def create_temp_table(self, db_session):
        temp_table_sql = """
            create table temp_install_info -- 安装信息完成事件也需要使用，所以 create 实体表
                (
                    muid      varchar(32),
                    country   varchar(32),
                    ins_time  timestamp,
                    app_name  varchar(32)
                );
        """
        # db_session.execute(temp_table_sql)
        print(temp_table_sql)

    def fill_temp_table(self, db_session, country_map):
        for i in range(0, (self._date_end - self._date_start).days + 1, 3):
            day = self._date_start + timedelta(days=i)
            day_head_str = day.strftime('%Y-%m-%d')
            day_tail = day + timedelta(days=self._date_step)
            day_tail_str = day_tail.strftime('%Y-%m-%d')

            for app_name in self._app_list:
                sql_statement = """
                insert into temp_install_info
                    select 
                        md.muid,
                        info.country_code as country,
                        info.date_occurred as ins_time,
                        '{app_name_iter}' as app_name
                    from 
                        kch_{app_name_iter}_install_info info
                    inner join 
                        muid_dimension md 
                    on md.muid = info.kochava_device_id
                    where 1 = 1
                        {country_filter}
                        and trunc(info.date_occurred) >= '{day_head_str}'
                        and trunc(info.date_occurred) < '{day_tail_str}'
                        and trunc(info.date_occurred) <= '{date_end}';
                """.format(
                    date_start=self._date_start.strftime('%Y-%m-%d'),
                    date_end=self._date_end.strftime('%Y-%m-%d'),
                    app_name_iter=app_name,
                    day_head_str=day_head_str,
                    day_tail_str=day_tail_str,
                    country_filter="and info.country_code in ({countries})".format(
                        countries="'" + "','".join(country_map.get(app_name)) + "'"
                    ),
                )
                # db_session.execute(sql_statement)
                print(sql_statement)

    def run_query(self, db_session, country_map):
        query_sql = """
            with psd_ins as (
                select info.muid,
                       info.country,
                       trunc(info.ins_time),
                       info.app_name,
                       count(1) as impr_type
                from spectrum.fact_ivt_poseidon_log log
                         inner join temp_install_info info
                                    on info.muid = log.muid
                                        and trunc(log_time) >= '{date_start}'
                                        and trunc(log_time) <= '{date_end}'
                                        and action_type = 'impression'
                                        and ad_format in ('interstitial', 'rewardedvideo')
                where 1 = 1
                  and log.action_time <= dateadd(day, {date_step}, info.ins_time)
                group by info.muid,
                         info.country,
                         trunc(info.ins_time),
                         info.app_name)
            select log.country,
                   log.impr_type,
                   count(log.muid)                                                                                 as muid_count,
                   sum(muid_count)
                   over (partition by log.app_name, log.country order by log.impr_type rows between current row and unbounded following) as sum_count,
                   log.app_name
            from psd_ins log
            group by log.country,
                     log.impr_type,
                     log.app_name
            order by log.country,
                     log.impr_type;
            """.format(
                date_start=self._date_start.strftime('%Y-%m-%d'),
                date_end=self._date_end.strftime('%Y-%m-%d'),
                date_step=self._date_step,

        )
        # rs = db_session.execute(query_sql)
        print(query_sql)
        # return rs


    def interstitial_and_rewardedvideo_calc(self):
        country_map = self.get_country_filter()
        rowset_list = []
        db_session = self.db_conn()

        self.create_temp_table(db_session)
        self.fill_temp_table(db_session, country_map)
        rowset = self.run_query(db_session, country_map)

        rowset_list.append(rowset)
        self.get_result_csv(rowset_list, db_session)


    def get_result_csv(self, rowset_list, db_session):
        dnu_map = {}
        for app_name in self._app_list:
            dnu_map[app_name] = self.get_sum_dnu_map(app_name)

        self.session_close(self, db_session)

        filename = self.__class__.__name__
        filepath = f'/Users/long.tian/Desktop/Applovin_res/{filename}.csv'
        with open(filepath, 'w') as file:
            file.write(','.join(['m', 'app_name', 'country', 'dnu', 'eu', 'percentage']))
            file.write('\n')
            for rs in rowset_list:
                for r in rs:
                    country = r[0]
                    complete_type = r[1]
                    muid_count = r[2]
                    sum_count = r[3]
                    app_name = r[4]
                    dnu_sum = dnu_map[app_name].get(country)
                    persent = 1.0 * sum_count / dnu_sum
                    data = ','.join([str(complete_type), app_name, country, str(dnu_sum), str(sum_count), str(persent)])
                    file.write(data)
                    file.write('\n')

    def session_close(self, db_session):
        # 安装信息完成事件也需要使用，所以实体表暂不删除
        # drop_temp_table = """
        #     drop table if exists temp_install_info;
        # """
        # db_session.execute(drop_temp_table)
        db_session.commit()

if __name__ == '__main__':
    start = datetime.now()
    print('开始时间' + start.strftime('%Y-%m-%d %H:%M:%S'))

    app = applovin_reward_video_calc()
    res = app.interstitial_and_rewardedvideo_calc()

    end = datetime.now()
    duration = end - start
    print('结束时间' + end.strftime('%Y-%m-%d %H:%M:%S') + ', 用时' + str(duration.seconds) + '秒。')
