from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date, timedelta, datetime
from rock.common import log

logger = log.get_logger('RewardVideo')

class RetentionCalc:

    def __init__(self, execute_date):
        self.execute_date = execute_date

        # self._app_list = ['saori_gp', 'dohko_gp', 'aiolos_gp','saori_ip', 'dohko_ip', 'aiolos_ip','saga_gp']
        self._app_list = ['aiolos_gp']
        self._install_date_end = datetime.strptime(execute_date, "%Y-%m-%d")
        self._install_date_start = self._install_date_end + timedelta(days=-37)
        self._log_date_step = -1
        self._app_package_name_map = {
            'saori_gp': 'art.color.planet.paint.by.number.game.puzzle.free',
            'dohko_gp': 'art.color.planet.oil.paint.canvas.number.free',
            'aiolos_gp': 'art.color.planet.jigsaw.puzzle.online.free',
            'saga_gp': 'happy.puzzle.merge.block.shoot2048.number.game.free',
            'saori_ip': 'art.color.planet.paint.by.number.game.puzzle',
            'dohko_ip': 'art.color.planet.oil.paint.canvas.number',
            'aiolos_ip': 'art.color.planet.jigsaw.puzzle.online',
        }
    

    def db_conn(self):
        engine_PROD = create_engine('postgres://gv_developer:AjFtinLDMQ0w7i0f@3.230.194.153:5200/db_redshift_gv')
        dbsession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_PROD))
        return dbsession()

    def create_temp_table(self, db_session):
        temp_table_sql = """
            create temp table temp_psd_log
                (
                    muid              varchar(64),
                    app_package_name  varchar(64),
                    action_date       date
                );
        """
        db_session.execute(temp_table_sql)
        # print(temp_table_sql)

    def fillin_temp_table(self, db_session):

        sql_statement = """
            insert into temp_psd_log
            select muid,
                   app_package_name,
                   trunc(convert_timezone('Asia/Shanghai', log.action_time)) as action_date
            from spectrum.fact_ivt_poseidon_log log
            where 1 = 1
              and trunc(log.log_time) = '{log_date_start}'
            group by muid, app_package_name, action_date 
        """.format(
            log_date_start=(self._install_date_end + timedelta(days=self._log_date_step)).strftime('%Y-%m-%d'),
        )

        db_session.execute(sql_statement)
        # print(sql_statement)

    def init_data_by_execute_date(self, db_session, execute_date):
        init_sql = """
            delete from 
                ads_posd_kch_retention_activities
            where 
                dateadd(day, day_dimension, install_date) = '{execute_date}';
        """.format(
            execute_date=execute_date,
        )

        db_session.execute(init_sql)
        # print(init_sql)


    def insert_calc(self, db_session):

        for app_name in self._app_list:
            sql_statement = """
                insert into ads_posd_kch_retention_activities
                with install_info as (
                    select md.muid,
                           trunc(convert_timezone('Asia/Shanghai', info.date_occurred)) as install_date
                    from kch_{app_name}_install_info info    -- todo 源表待定，可从维表拿 muid 及 install_date 
                             inner join muid_dimension md
                                        on md.kch_id = info.kochava_device_id
                    where 1 = 1
                      and install_date >= '{date_start}'
                      and install_date <= '{date_end}'
                    group by md.muid, install_date
                ),
                     psd_log as (
                         select muid,
                                action_date
                         from temp_psd_log log
                         where 1 = 1
                           {app_package_name_filter}
                         group by muid, action_date
                     ),
                     kch_log as (
                         select md.muid,
                                trunc(convert_timezone('Asia/Shanghai', log.date_occurred)) as action_date
                         from kch_{app_name}_event_info log
                                  inner join muid_dimension md
                                             on md.kch_id = log.kochava_device_id
                         where 1 = 1
                           and trunc(log.date_occurred) = '{log_date_start}'
                         group by muid, action_date
                     ),
                     ins_psd_log as (
                         select info.muid,
                                info.install_date,
                                datediff(day, info.install_date, log.action_date) as day_dimension
                         from install_info info
                                  inner join psd_log log
                                             on log.muid = info.muid
                         where 1 = 1
                            and day_dimension >= 0
                            and day_dimension <= 37
                     ),
                     ins_kch_log as (
                         select info.muid,
                                info.install_date,
                                datediff(day, info.install_date, log.action_date) as day_dimension
                         from install_info info
                                  inner join kch_log log
                                             on log.muid = info.muid
                         where 1 = 1
                            and day_dimension >= 0
                            and day_dimension <= 37
                     )
                select case when iklog.muid is not null then iklog.muid else iplog.muid end                            as muid,
                       case when iklog.install_date is not null then iklog.install_date else iplog.install_date end    as install_date,
                       case when iklog.day_dimension is not null then iklog.day_dimension else iplog.day_dimension end as day_dimension,
                       case when iplog.day_dimension is not null then 1 else 0 end                                     as poseidon_active,
                       case when iklog.day_dimension is not null then 1 else 0 end                                     as kch_active
                from ins_psd_log iklog
                         full join
                     ins_kch_log iplog
                     on
                                 iklog.day_dimension = iplog.day_dimension
                             and iklog.muid = iplog.muid
                             and iklog.install_date = iplog.install_date;
            """.format(
                app_name=app_name,
                date_start=self._install_date_start.strftime('%Y-%m-%d'),
                date_end=self._install_date_end.strftime('%Y-%m-%d'),
                log_date_start=(self._install_date_end + timedelta(days=self._log_date_step)).strftime('%Y-%m-%d'),
                app_package_name_filter="and log.app_package_name = '{package_name}'".format(
                    package_name=self._app_package_name_map.get(app_name)
                )
            )

            db_session.execute(sql_statement)
            # print(sql_statement)

    def session_close(self, db_session):
        try:
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def run_calc(self):
        db_session = self.db_conn()
        self.create_temp_table(db_session)
        self.fillin_temp_table(db_session)
        # self.init_data_by_execute_date(db_session, self.execute_date)
        self.insert_calc(db_session)
        self.session_close(db_session)

if __name__ == '__main__':

    app = RetentionCalc('2021-08-20')
    app.run_calc()