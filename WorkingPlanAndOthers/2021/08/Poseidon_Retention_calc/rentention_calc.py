from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date, timedelta, datetime


class RetentionCalc():

    _app_list = ['saori_gp', 'dohko_gp', 'aiolos_gp','saori_ip', 'dohko_ip', 'aiolos_ip','saga_gp']
    _install_date_end = date(2021, 8, 19)
    _install_date_start = _install_date_end + timedelta(days=-37)
    _log_date_step = -1
    _app_package_name_map = {
        'saori_gp': 'art.color.planet.paint.by.number.game.puzzle.free',
        'dohko_gp': 'art.color.planet.oil.paint.canvas.number.free',
        'aiolos_gp': 'art.color.planet.jigsaw.puzzle.online.free',
        'saga_gp': 'happy.puzzle.merge.block.shoot2048.number.game.free',
        'saori_ip': 'art.color.planet.paint.by.number.game.puzzle',
        'dohko_ip': 'art.color.planet.oil.paint.canvas.number',
        'aiolos_ip': 'art.color.planet.jigsaw.puzzle.online',
    }



    def calc(self):

        for app_name in self._app_list:
            sql_statement = """
                with install_info as (
                    select md.muid,
                           trunc(convert_timezone('Asia/Shanghai', info.date_occurred)) as install_date
                    from kch_{app_name}_install_info info
                             inner join muid_dimension md
                                        on md.kch_id = info.kochava_device_id
                    where 1 = 1
                      and install_date >= '{date_start}'
                      and install_date <= '{date_end}'
                    group by md.muid, trunc(convert_timezone('Asia/Shanghai', info.date_occurred))
                ),
                     psd_log as (
                         select muid,
                                trunc(convert_timezone('Asia/Shanghai', log.action_time)) as action_date
                         from spectrum.fact_ivt_poseidon_log log
                         where 1 = 1
                           {app_package_name_filter}
                           and trunc(log.log_time) = '{log_date_start}'
                         group by muid, trunc(convert_timezone('Asia/Shanghai', log.action_time))
                     ),
                     kch_log as (
                         select md.muid,
                                trunc(convert_timezone('Asia/Shanghai', log.date_occurred)) as action_date
                         from kch_{app_name}_event_info log
                                  inner join muid_dimension md
                                             on md.kch_id = log.kochava_device_id
                         where 1 = 1
                           and trunc(log.date_occurred) = '{log_date_start}'
                         group by muid, trunc(convert_timezone('Asia/Shanghai', log.date_occurred))
                     ),
                     ins_psd_log as (
                         select info.muid,
                                datediff(day, info.install_date, log.action_date) as day_dimension
                         from install_info info
                                  inner join psd_log log
                                             on log.muid = info.muid
                     ),
                     ins_kch_log as (
                         select info.muid,
                                datediff(day, info.install_date, log.action_date) as day_dimension
                         from install_info info
                                  inner join kch_log log
                                             on log.muid = info.muid
                     )
                select iklog.muid,
                       iklog.day_dimension,
                       case when iklog.day_dimension is not null then 1 else 0 end,
                       case when iplog.day_dimension is not null then 1 else 0 end
                from ins_kch_log iklog
                         left join ins_psd_log iplog on iklog.day_dimension = iplog.day_dimension and iklog.muid = iplog.muid
                union
                select iplog.muid,
                       iplog.day_dimension,
                       case when iklog.day_dimension is not null then 1 else 0 end,
                       case when iplog.day_dimension is not null then 1 else 0 end
                from ins_kch_log iklog
                         right join ins_psd_log iplog on iklog.day_dimension = iplog.day_dimension and iklog.muid = iplog.muid;
            """.format(
                app_name=app_name,
                date_start=self._install_date_start.strftime('%Y-%m-%d'),
                date_end=self._install_date_end.strftime('%Y-%m-%d'),
                log_date_start=(self._install_date_end + timedelta(days=self._log_date_step)).strftime('%Y-%m-%d'),
                app_package_name_filter="and log.app_package_name = '{package_name}'".format(
                    package_name=self._app_package_name_map.get(app_name)
                )
            )


            print(sql_statement)

RetentionCalc().calc()