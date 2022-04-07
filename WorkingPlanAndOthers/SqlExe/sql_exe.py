from datetime import datetime, timedelta
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def get_date_range(date_start, date_end):
    """
    :return: 返回从date_start到date_end的所有日期的列表
    """
    dates = []
    dt = datetime.strptime(date_start, "%Y-%m-%d")
    dt_end = datetime.strptime(date_end, "%Y-%m-%d")
    while dt <= dt_end:
        dates.append(dt.strftime("%Y-%m-%d"))
        dt = dt + timedelta(1)
    return dates


date_list = get_date_range('2022-03-29', '2022-04-05')

engine = create_engine('postgresql://gv_developer:AjFtinLDMQ0w7i0f@3.230.194.153:5200/db_redshift_gv')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))()

for exe_date in date_list:
    sql_statement = """
insert into temp_mid_ilrd_should_display_20220406(bj_date, app_name, country, placement, should_display, impr)
with log_temp as (
    select
        trunc(dateadd(hour, 8, service_log_time))                        as bj_date,
        (case app_package_name
             when 'art.color.planet.paint.by.number.game.puzzle.free'
                 then 'saori_gp'
             when 'art.color.planet.paint.by.number.game.puzzle'
                 then 'saori_ip'
             when 'happy.puzzle.merge.block.shoot2048.number.game.free'
                 then 'saga_gp'
             when 'art.color.planet.jigsaw.puzzle.online'
                 then 'aiolos_ip'
             when 'art.color.planet.oil.paint.canvas.number'
                 then 'dohko_ip'
             when 'art.color.planet.oil.paint.canvas.number.free'
                 then 'dohko_gp'
             when 'art.color.planet.jigsaw.puzzle.online.free'
                 then 'aiolos_gp'
             when 'happy.puzzle.merge.block.shoot2048.number.game'
                 then 'saga_ip'
                 else 'null' end)                                        as app_name,
        muid,
        placement_name,
        sum(case action_type when 'ad_should_display' then 1 else 0 end) as should_display,
        sum(case action_type
                when 'impression'
                    then 1 * (
                    case
                        when 1 != 1
                            then 1

                        when app_package_name = 'art.color.planet.jigsaw.puzzle.online' and app_version_code >= 27
                            and vendor = 'amazon'
                            then 1


                        when app_package_name = 'art.color.planet.jigsaw.puzzle.online' and app_version_code >= 17
                            and vendor = 'amazon'
                            then 0.33

                            else 1
                        end
                    )
                    else 0 end)                                          as impr
    from spectrum.fact_ivt_poseidon_log
    where action_type in ('ad_should_display', 'impression')
      and datediff(
            hour,
            '{exe_date}',
            dateadd(hour, 8, log_time)
        ) between -1 and 24
      and trunc(dateadd(hour, 8, service_log_time)) = '{exe_date}'
      and (
            (app_package_name = 'art.color.planet.paint.by.number.game.puzzle.free' and app_version_code >= 31) or
            (app_package_name = 'art.color.planet.paint.by.number.game.puzzle' and app_version_code >= 21) or
            (app_package_name = 'happy.puzzle.merge.block.shoot2048.number.game.free' and app_version_code >= 4) or
            (app_package_name = 'art.color.planet.jigsaw.puzzle.online' and app_version_code >= 17) or
            (app_package_name = 'art.color.planet.oil.paint.canvas.number' and app_version_code >= 37) or
            (app_package_name = 'art.color.planet.oil.paint.canvas.number.free' and app_version_code >= 43) or
            (app_package_name = 'art.color.planet.jigsaw.puzzle.online.free' and app_version_code >= 12) or
            (app_package_name = 'happy.puzzle.merge.block.shoot2048.number.game' and app_version_code >= 2)
        )
    group by app_package_name,
             muid,
             trunc(dateadd(hour, 8, service_log_time)),
             placement_name
)
select
    lt.bj_date,
    lt.app_name,
    case
        when md.kch_country is not null
            then md.kch_country
            else 'Unknown' end as res_country,
    lt.placement_name,
    sum(lt.should_display)     as sum_should_display,
    sum(lt.impr)::int          as sum_impr
from log_temp                lt
    left join muid_dimension md
              on md.muid = lt.muid
group by lt.bj_date,
         lt.app_name,
         res_country,
         lt.placement_name
;
""".format(exe_date=exe_date)

    # print(sql_statement)

    start_date = datetime.utcnow() + timedelta(hours=8)
    print(f'{exe_date} Start at {start_date.strftime("%Y-%m-%d %H:%M:%S")}')
    session.execute(sql_statement)
    session.commit()
    end_date = datetime.utcnow() + timedelta(hours=8)
    print(f'{exe_date} Done! at {end_date.strftime("%Y-%m-%d %H:%M:%S")}')
    sleep(2)


