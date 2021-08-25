from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date, timedelta, datetime
from rock.common import log

logger = log.get_logger('RewardVideo')


class applovin_reward_video_calc:
    _app_list = ['saori_gp', 'dohko_gp', 'aiolos_gp', 'saori_ip', 'dohko_ip', 'aiolos_ip', 'saga_gp']
    _date_start = date(2021, 7, 20)
    _date_end = date(2021, 7, 23)
    _date_step = 2

    def db_conn(self):
        engine_PROD = create_engine('postgres://gv_developer:AjFtinLDMQ0w7i0f@3.230.194.153:5200/db_redshift_gv')
        dbsession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_PROD))
        return dbsession()

    def get_country_filter(self):
        country_map = {'dohko_gp': ['US', 'IN', 'RU'],
                       'saori_gp': ['IN', 'BR', 'MX', 'EG', 'PK', 'CO', 'PE', 'AR', 'PH', 'ID', 'TR', 'DZ', 'UZ', 'GT',
                                    'RU', 'US', 'EC', 'BO', 'TH', 'MY', 'BD', 'HN', 'KZ', 'DO', 'LB', 'CL', 'SA', 'LK',
                                    'JO'],
                       'aiolos_gp': ['BR', 'MX', 'AR', 'US'],
                       'aiolos_ip': ['US', 'MX', 'BR'],
                       'saori_ip': ['US', 'SA', 'BR'],
                       'dohko_ip': ['US', 'CA', 'RU'],
                       'saga_gp': ['BR', 'PH', 'RU', 'US'],
                       }

        return country_map

    def get_sum_dnu_map(self, app_name, db_session):
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
        rs = db_session.execute(sql_statement)
        country_map = {}
        for r in rs:
            country = r[0]
            sum_dnu = r[1]
            country_map.setdefault(country)
            country_map[country] = sum_dnu
        return country_map

    def create_temp_table(self, db_session):
        temp_table_sql = """
            create temp table temp_install_info
                (
                    muid      varchar(64),
                    country   varchar(32),
                    ins_time  timestamp,
                    app_name  varchar(32)
                );
        """
        db_session.execute(temp_table_sql)
        temp_table_sql = """
            create temp table temp_count_info
                (

                      date_range varchar(64),
                        app_name varchar(32),
                       country varchar(32),
                       impr_type int,
                       c int
                );
        """
        db_session.execute(temp_table_sql)

    def fill_temp_table(self, db_session, country_map):
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
                on md.kch_id = info.kochava_device_id
                where 1 = 1
                    {country_filter}
                    and trunc(info.date_occurred) >= '{date_start}'
                    and trunc(info.date_occurred) <= '{date_end}';
            """.format(
                date_start=self._date_start.strftime('%Y-%m-%d'),
                date_end=self._date_end.strftime('%Y-%m-%d'),
                app_name_iter=app_name,
                country_filter="and info.country_code in ({countries})".format(
                    countries="'" + "','".join(country_map.get(app_name)) + "'"
                ),
            )
            db_session.execute(sql_statement)
            db_session.commit()

    def run_query(self, db_session):
        for i in range(0, (self._date_end - self._date_start).days + 1, self._date_step):
            day = self._date_start + timedelta(days=i)
            day_head_str = day.strftime('%Y-%m-%d')
            day_tail = day + timedelta(days=self._date_step)
            day_tail_str = day_tail.strftime('%Y-%m-%d')

            query_sql = """
                insert into temp_count_info
                with psd_ins as (
                    select info.muid,
                           info.country,
                           trunc(info.ins_time),
                           info.app_name,
                           count(1) as impr_type
                    from spectrum.fact_ivt_poseidon_log log
                             inner join temp_install_info info
                                        on info.muid = log.muid

                                            and trunc(info.ins_time) >= '{date_head_str}'
                                            and trunc(info.ins_time) < '{date_tail_str}'
                                            and trunc(log_time) >= '{date_head_str}'
                                            and trunc(log_time) <= '{date_tail_str}'
                                            and action_type = 'impression'
                                            and ad_format in ('interstitial', 'rewardedvideo')
                    where 1 = 1
                      and log.action_time <= dateadd(day, 1, info.ins_time)
                    group by info.muid,
                             info.country,
                             trunc(info.ins_time),
                             info.app_name)
                select 
                        '{date_range}' as date_range,
                       log.app_name,
                       log.country,
                       log.impr_type,
                       count(log.muid)                                                                                 
                from psd_ins log
                group by log.country,
                         log.impr_type,
                         log.app_name
                order by log.country,
                         log.impr_type;
                """.format(
                date_head_str=day_head_str,
                date_tail_str=day_tail_str,
                date_range=f'{day_head_str}_{day_tail_str}',
            )
            logger.info("查询开始！", f'{day_head_str}_{day_tail_str}')
            db_session.execute(query_sql)
        logger.info("最终查询开始！")
        rs = db_session.execute("""
            select
                app_name, country, impr_type,
                sum(c) as muid_count,
                sum(muid_count) over (partition by app_name, country order by impr_type rows between current row and unbounded following) as sum_count
            from
                temp_count_info
            group by
                app_name, country, impr_type
        """).fetchall()
        logger.info("最终查询结束！")
        return rs

    def interstitial_and_rewardedvideo_calc(self):
        country_map = self.get_country_filter()
        db_session = self.db_conn()

        self.create_temp_table(db_session)
        self.fill_temp_table(db_session, country_map)
        rowset = self.run_query(db_session)

        logger.info("写入csv！")
        self.get_result_csv(rowset, db_session)

    def get_result_csv(self, rowset_list, db_session):
        dnu_map = {}
        for app_name in self._app_list:
            dnu_map[app_name] = self.get_sum_dnu_map(app_name, db_session)

        try:
            db_session.commit()
        except:
            db_session.rollback()
            raise

        filename = self.__class__.__name__
        filepath = f'./{filename}.csv'
        with open(filepath, 'w') as file:
            file.write(','.join(['m', 'app_name', 'country', 'dnu', 'eu', 'percentage', 'event_detail_cnt']))
            file.write('\n')
            for r in rowset_list:
                country = r[1]
                complete_type = r[2]
                muid_count = r[3]
                sum_count = r[4]
                app_name = r[0]
                dnu_sum = dnu_map[app_name].get(country)
                persent = 1.0 * sum_count / dnu_sum
                data = ','.join([str(complete_type), app_name, country, str(dnu_sum), str(sum_count), str(persent),
                                 str(muid_count)])
                file.write(data)
                file.write('\n')


if __name__ == '__main__':
    start = datetime.now()
    logger.info('开始时间')

    app = applovin_reward_video_calc()
    res = app.interstitial_and_rewardedvideo_calc()

    end = datetime.now()
    duration = end - start
    print('结束时间' + end.strftime('%Y-%m-%d %H:%M:%S') + ', 用时' + str(duration.seconds) + '秒。')
