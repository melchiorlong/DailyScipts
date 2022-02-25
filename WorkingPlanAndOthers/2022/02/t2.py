from datetime import datetime, timedelta
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


date_list = get_date_range('2022-02-19', '2022-02-21')

engine = create_engine('postgresql://gv_developer:AjFtinLDMQ0w7i0f@3.230.194.153:5200/db_redshift_gv')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))()

for exe_date in date_list:
    sql_statement = """
insert into temp_ads_mkt_mediation_monitoring_20220224 (country,
                                          app_name,
                                          placement_name,
                                          rev_bj_date,
                                          version,
                                          dau,
                                          impression_cnt,
                                          ads_should_dis_cnt,
                                          ads_rev)
with psd_log_all           as (
    select
        log.muid,
        action_type,
        placement_name,
        app_version_code,
        ilrd_country,
        ilrd_mediation_type,
        (case app_package_name
             when 'art.color.planet.oil.paint.canvas.number'
                 then 'dohko_ip'
             when 'art.color.planet.oil.paint.canvas.number.free'
                 then 'dohko_gp'
             when 'art.color.planet.paint.by.number.game.puzzle.free'
                 then 'saori_gp'
             when 'art.color.planet.paint.by.number.game.puzzle'
                 then 'saori_ip'
             when 'art.color.planet.jigsaw.puzzle.online.free'
                 then 'aiolos_gp'
             when 'art.color.planet.jigsaw.puzzle.online'
                 then 'aiolos_ip'
             when 'happy.puzzle.merge.block.shoot2048.number.game.free'
                 then 'saga_gp'
             when 'happy.puzzle.merge.block.shoot2048.number.game'
                 then 'saga_ip'
                 else 'null' end)                          as app_name,
        case
            when (app_name = 'dohko_ip' and app_version_code >= 47 and ilrd_mediation_type = 2)
                then 'Max'

            when (app_name = 'dohko_ip' and app_version_code >= 47 and ilrd_mediation_type = 3)
                then 'Admob'

            when (app_name = 'dohko_ip' and app_version_code >= 46)
                then 'Max'
            when (app_name = 'dohko_ip' and app_version_code <= 46)
                then 'Mopub'

            when (app_name = 'dohko_gp' and app_version_code >= 51 and ilrd_mediation_type = 2)
                then 'Max'

            when (app_name = 'dohko_gp' and app_version_code >= 51 and ilrd_mediation_type = 3)
                then 'Admob'

            when (app_name = 'dohko_gp' and app_version_code >= 50)
                then 'Max'
            when (app_name = 'dohko_gp' and app_version_code <= 50)
                then 'Mopub'

            when (app_name = 'saori_gp' and app_version_code >= 43 and ilrd_mediation_type = 2)
                then 'Max'

            when (app_name = 'saori_gp' and app_version_code >= 43 and ilrd_mediation_type = 3)
                then 'Admob'

            when (app_name = 'saori_gp' and app_version_code >= 42)
                then 'Max'
            when (app_name = 'saori_gp' and app_version_code <= 42)
                then 'Mopub'

            when (app_name = 'saori_ip' and app_version_code >= 29 and ilrd_mediation_type = 2)
                then 'Max'

            when (app_name = 'saori_ip' and app_version_code >= 29 and ilrd_mediation_type = 3)
                then 'Admob'

            when (app_name = 'saori_ip' and app_version_code >= 28)
                then 'Max'
            when (app_name = 'saori_ip' and app_version_code <= 28)
                then 'Mopub'

            when (app_name = 'aiolos_gp' and app_version_code >= 999 and ilrd_mediation_type = 2)
                then 'Max'

            when (app_name = 'aiolos_gp' and app_version_code >= 999 and ilrd_mediation_type = 3)
                then 'Admob'

            when (app_name = 'aiolos_gp' and app_version_code >= 999)
                then 'Max'
            when (app_name = 'aiolos_gp' and app_version_code <= 999)
                then 'Mopub'

            when (app_name = 'aiolos_ip' and app_version_code >= 24 and ilrd_mediation_type = 2)
                then 'Max'

            when (app_name = 'aiolos_ip' and app_version_code >= 24 and ilrd_mediation_type = 3)
                then 'Admob'

            when (app_name = 'aiolos_ip' and app_version_code >= 23)
                then 'Max'
            when (app_name = 'aiolos_ip' and app_version_code <= 23)
                then 'Mopub'

            when (app_name = 'saga_gp' and app_version_code >= 999 and ilrd_mediation_type = 2)
                then 'Max'

            when (app_name = 'saga_gp' and app_version_code >= 999 and ilrd_mediation_type = 3)
                then 'Admob'

            when (app_name = 'saga_gp' and app_version_code >= 999)
                then 'Max'
            when (app_name = 'saga_gp' and app_version_code <= 999)
                then 'Mopub'

            when (app_name = 'saga_ip' and app_version_code >= 999 and ilrd_mediation_type = 2)
                then 'Max'

            when (app_name = 'saga_ip' and app_version_code >= 999 and ilrd_mediation_type = 3)
                then 'Admob'

            when (app_name = 'saga_ip' and app_version_code >= 999)
                then 'Max'
            when (app_name = 'saga_ip' and app_version_code <= 999)
                then 'Mopub'
                else 'Unknown' end                         as version,
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
      and app_package_name in ('art.color.planet.jigsaw.puzzle.online', 'art.color.planet.oil.paint.canvas.number.free',
                               'art.color.planet.oil.paint.canvas.number',
                               'art.color.planet.paint.by.number.game.puzzle.free',
                               'art.color.planet.paint.by.number.game.puzzle')
),
     log_temp_all          as (
         select
             rev_bj_date,
             placement_name,
             ilrd_country                                                       as country,
             app_name,
             version,
             sum(case when action_type = 'ad_should_display' then 1 else 0 end) as should_cnt,
             sum(case when action_type = 'impression' then 1 else 0 end)        as impr_cnt,
             sum(fb_impr)                                                       as facebook_ads_impr_cnt,
             sum(ads_rev_without_fb)                                            as ads_rev_without_fb
         from psd_log_all
         where placement_name != ''
         group by rev_bj_date,
                  placement_name,
                  version,
                  app_name,
                  ilrd_country
     ),
     log_temp_muid_country as (
         select
             rev_bj_date,
             placement_name,
             muid,
             app_name,
             version,
             sum(case when action_type = 'ad_should_display' then 1 else 0 end) as should_cnt,
             sum(case when action_type = 'impression' then 1 else 0 end)        as impr_cnt,
             sum(fb_impr)                                                       as facebook_ads_impr_cnt,
             sum(ads_rev_without_fb)                                            as ads_rev_without_fb
         from psd_log_all
         where placement_name != ''
         group by rev_bj_date,
                  placement_name,
                  version,
                  app_name,
                  muid
     ),
     log_temp_country      as (
         select
             log.rev_bj_date,
             log.placement_name,
             log.app_name,
             log.version,
             md.kch_country             as country,
             sum(should_cnt)            as sum_should_cnt,
             sum(impr_cnt)              as sum_impr_cnt,
             sum(facebook_ads_impr_cnt) as sum_facebook_ads_impr_cnt,
             sum(ads_rev_without_fb)    as sum_ads_rev_without_fb
         from log_temp_muid_country    log
             inner join muid_dimension md on md.muid = log.muid
         group by log.rev_bj_date,
                  log.placement_name,
                  log.app_name,
                  log.version,
                  md.kch_country
     ),
     cpm_temp              as (
         select distinct
             trunc(convert_timezone('Asia/Shanghai', date)) as cpm_date,
             country,
             app_name,
             fb_cpm
         from mid_ilrd_dh_fb_cpm
         where 1 = 1
           and cpm_date >= '{exe_date}'
           and cpm_date <= '{exe_date}'
           and app_name in ('aiolos_ip', 'dohko_gp', 'dohko_ip', 'saori_gp', 'saori_ip')
     ),
     country_dau_temp      as (
         select
             rev_bj_date,
             app_name,
             muid,
             version,
             count(distinct muid) as no_pl_dau_temp
         from psd_log_all
         where action_type = 'session_start'
         group by rev_bj_date,
                  app_name,
                  version,
                  muid
     ),
     no_placement_dau      as (
         select
             cdt.rev_bj_date,
             cdt.app_name,
             md.kch_country          as country,
             cdt.version,
             sum(cdt.no_pl_dau_temp) as sum_no_pl_dau_temp
         from country_dau_temp         cdt
             inner join muid_dimension md on md.muid = cdt.muid
         group by cdt.rev_bj_date,
                  cdt.app_name,
                  cdt.version,
                  md.kch_country
         union all
         select
             rev_bj_date,
             app_name,
             'All'                as country,
             version,
             count(distinct muid) as sum_no_pl_dau_temp
         from psd_log_all
         where action_type = 'session_start'
         group by rev_bj_date,
                  app_name,
                  version
     ),
     rs_1                  as (
         select
             lt.rev_bj_date,
             lt.placement_name,
             version,
             lt.app_name,
             lt.country,
             sum(lt.sum_should_cnt)              as ads_should_dis_cnt,
             sum(lt.sum_impr_cnt)                as impression_cnt,
             sum(nvl((case
                          when ct.fb_cpm is not null
                              then lt.sum_facebook_ads_impr_cnt * ct.fb_cpm
                              else 0 end), 0))
                 +
             sum(nvl(sum_ads_rev_without_fb, 0)) as ads_rev
         from log_temp_country  lt
             left join cpm_temp ct
                       on ct.country = lt.country
                           and ct.cpm_date = lt.rev_bj_date
                           and ct.app_name = lt.app_name
         group by rev_bj_date,
                  placement_name,
                  lt.app_name,
                  version,
                  lt.country
         union all
         select
             rev_bj_date,
             placement_name,
             version,
             lt.app_name,
             'All'                           as country,
             sum(should_cnt)                 as ads_should_dis_cnt,
             sum(impr_cnt)                   as impression_cnt,
             sum(nvl((case
                          when ct.fb_cpm is not null
                              then lt.facebook_ads_impr_cnt * ct.fb_cpm
                              else 0 end), 0))
                 +
             sum(nvl(ads_rev_without_fb, 0)) as ads_rev
         from log_temp_all      lt
             left join cpm_temp ct
                       on ct.country = lt.country
                           and ct.cpm_date = lt.rev_bj_date
                           and ct.app_name = lt.app_name
         group by rev_bj_date,
                  placement_name,
                  lt.app_name,
                  version
     )
select
    rs_1.country,
    rs_1.app_name,
    rs_1.placement_name,
    rs_1.rev_bj_date,
    rs_1.version,
    dau_temp.sum_no_pl_dau_temp,
    rs_1.impression_cnt,
    rs_1.ads_should_dis_cnt,
    rs_1.ads_rev
from rs_1
    join no_placement_dau dau_temp
         on rs_1.rev_bj_date = dau_temp.rev_bj_date
             and rs_1.version = dau_temp.version
             and rs_1.app_name = dau_temp.app_name
             and rs_1.country = dau_temp.country
order by rs_1.rev_bj_date,
         rs_1.version;

""".format(
        exe_date=exe_date
    )
    print(exe_date + ' Start')
    # print(sql_statement)
    session.execute(sql_statement)
