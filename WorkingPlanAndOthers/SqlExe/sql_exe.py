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


date_list = get_date_range('2022-03-05', '2022-03-06')

engine = create_engine('postgresql://gv_developer:AjFtinLDMQ0w7i0f@3.230.194.153:5200/db_redshift_gv')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))()

for exe_date in date_list:
    sql_statement = """
        insert into temp_mediation_us_max_device_no2_20220308
        with psd_log_all           as (
            select
                log.muid,
                action_type,
                placement_name,
                app_version_code,
                (case app_package_name
                     when 'art.color.planet.oil.paint.canvas.number'
                         then 'dohko_ip'
                     when 'art.color.planet.paint.by.number.game.puzzle'
                         then 'saori_ip'
                     when 'art.color.planet.jigsaw.puzzle.online'
                         then 'aiolos_ip'
                         else 'null' end)                          as app_name,
                case
                    when (app_name = 'dohko_ip' and app_version_code < 47) or
                         (app_name = 'saori_ip' and app_version_code < 29) or
                         (app_name = 'aiolos_ip' and app_version_code < 24)
                        then 'Mopub'
                    when ilrd_mediation_type = 2
                        then 'Max'
                    when ilrd_mediation_type = 3
                        then 'Admob'
                        else 'Max' end                             as version
                    ,
                trunc(convert_timezone('Asia/Shanghai', log_time)) as log_bj_date,
                trunc(dateadd(
                        hour, 8,
                        case
                            when abs(datediff(day, action_time, service_log_time)) > 2
                                then service_log_time
                                else action_time end
                    ))                                             as rev_bj_date,
                case
                    when vendor = 'facebook' and action_type = 'impression'
                        then 1
                        else 0 end                                 as fb_impr,
                case
                    when
                        vendor not in ('facebook', 'innerpromote') and action_type = 'impression'
                        then ilrd_publisher_revenue
                        else 0
                    end                                            as ads_rev_without_fb
            from spectrum.fact_ivt_poseidon_log as log
            where 1 = 1
              and log_bj_date between dateadd(day, -2, '{exe_date}') and dateadd(day, 2, '{exe_date}')
              and rev_bj_date between '{exe_date}' and '{exe_date}'
              and ((app_name = 'dohko_ip' and app_version_code >= 47)
                or (app_name = 'saori_ip' and app_version_code >= 29)
                or (app_name = 'aiolos_ip' and app_version_code >= 24))
              and app_package_name in ('art.color.planet.jigsaw.puzzle.online',
                                       'art.color.planet.oil.paint.canvas.number',
                                       'art.color.planet.paint.by.number.game.puzzle')
        ),
             psd_device_temp       as (
                 select
                     log.*,
                     md.kch_country,
                     install.device_model
                 from psd_log_all                       log
                     inner join muid_dimension          md on md.muid = log.muid
                     inner join dwd_ua_kch_install_info install on install.kochava_device_id = md.kch_id
                 where md.kch_country = 'US'
                   and log.version = 'Max'
             ),
             log_temp_muid_country as (
                 select
                     rev_bj_date,
                     placement_name,
                     app_name,
                     version,
                     device_model,
                     kch_country                                                        as country,
                     sum(case when action_type = 'ad_should_display' then 1 else 0 end) as sum_should_cnt,
                     sum(case when action_type = 'impression' then 1 else 0 end)        as sum_impr_cnt,
                     sum(fb_impr)                                                       as sum_facebook_ads_impr_cnt,
                     sum(ads_rev_without_fb)                                            as sum_ads_rev_without_fb
                 from psd_device_temp
                 where placement_name != ''
                   and action_type in ('ad_should_display', 'impression')
                 group by rev_bj_date,
                          placement_name,
                          version,
                          app_name,
                          device_model,
                          kch_country
             ),
             cpm_temp              as (
                 select distinct
                     trunc(convert_timezone('Asia/Shanghai', date)) as cpm_date,
                     country,
                     app_name,
                     fb_cpm
                 from mid_ilrd_dh_fb_cpm
                 where 1 = 1
                   and country = 'US'
                   and cpm_date >= '{exe_date}'
                   and cpm_date <= '{exe_date}'
                   and app_name in ('aiolos_ip', 'dohko_ip', 'saori_ip')
             ),
             all_dau               as (
                 select
                     rev_bj_date,
                     app_name,
                     kch_country          as country,
                     version,
                     device_model,
                     count(distinct muid) as sum_no_pl_dau_temp
                 from psd_device_temp
                 where action_type = 'session_start'
                 group by rev_bj_date,
                          app_name,
                          version,
                          kch_country,
                          device_model
             ),
             rs_1                  as (
                 select
                     lt.rev_bj_date,
                     lt.placement_name,
                     version,
                     lt.app_name,
                     lt.country,
                     lt.device_model,
                     sum(lt.sum_should_cnt)              as ads_should_dis_cnt,
                     sum(lt.sum_impr_cnt)                as impression_cnt,
                     sum(nvl((case
                                  when ct.fb_cpm is not null
                                      then lt.sum_facebook_ads_impr_cnt * ct.fb_cpm
                                      else 0 end), 0))
                         +
                     sum(nvl(sum_ads_rev_without_fb, 0)) as ads_rev
                 from log_temp_muid_country lt
                     left join cpm_temp     ct
                                   on ct.cpm_date = lt.rev_bj_date
                                   and ct.app_name = lt.app_name
                 group by rev_bj_date,
                          placement_name,
                          lt.app_name,
                          version,
                          lt.country,
                          lt.device_model
             )
        select
            rs_1.country,
            rs_1.app_name,
            rs_1.placement_name,
            rs_1.rev_bj_date,
            rs_1.version,
            rs_1.device_model,
            nvl(dau_temp.sum_no_pl_dau_temp, 0) as dau,
            rs_1.impression_cnt,
            rs_1.ads_should_dis_cnt,
            rs_1.ads_rev
        from rs_1
            inner join all_dau dau_temp
                       on rs_1.rev_bj_date = dau_temp.rev_bj_date
                           and rs_1.version = dau_temp.version
                           and rs_1.app_name = dau_temp.app_name
                           and rs_1.country = dau_temp.country
                           and rs_1.device_model = dau_temp.device_model
        order by rs_1.app_name,
                 rs_1.device_model,
                 rs_1.placement_name,
                 rs_1.rev_bj_date,
                 rs_1.version;
""".format(exe_date=exe_date)

    # print(sql_statement)

    start_date = datetime.utcnow() + timedelta(hours=8)
    print(f'{exe_date} Start at {start_date.strftime("%Y-%m:%d %H:%M:%S")}')
    session.execute(sql_statement)
    session.commit()
    end_date = datetime.utcnow() + timedelta(hours=8)
    print(f'{exe_date} Done! at {end_date.strftime("%Y-%m:%d %H:%M:%S")}')
    sleep(2)


