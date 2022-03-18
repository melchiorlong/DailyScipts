with creawler_table as (
    select
        trunc(dateadd(hour, 8, date)) as bj_date,
        placement_name,
        sum(impr)                     as sum_impr
    from mid_dh_market_data
    where app_name = 'saori_ip'
      and dateadd(hour, 8, date) >= '2022-03-01'
      and dateadd(hour, 8, date) <= '2022-03-17'
    group by placement_name,
             bj_date
),
     psd_log        as (
         select
             trunc(dateadd(hour, 8, service_log_time))                          as bj_date,
             placement_name,
             sum(case when action_type = 'impression' then 1 else 0 end)        as sum_impr,
             sum(case when action_type = 'ad_should_display' then 1 else 0 end) as sum_ad_should_display,
             sum(case
                     when action_type = 'impression' and app_version_code > 28
                         then 1
                         else 0 end)                                            as sum_impression_Max
         from spectrum.fact_ivt_poseidon_log log
         where 1 = 1
           and action_type in ('impression', 'ad_should_display')
           and dateadd(hour, 8, log_time) >= '2022-03-01'
           and trunc(dateadd(hour, 8, service_log_time)) >= '2022-03-01'
           and trunc(dateadd(hour, 8, service_log_time)) <= '2022-03-17'
           and app_package_name = 'art.color.planet.paint.by.number.game.puzzle'
         group by bj_date,
                  placement_name
     )
select
    pl.bj_date,
    pl.placement_name,
    ct.sum_impr              as CrawlerTask_Impression,
    pl.sum_impr              as PSD_LOG_Impression,
    pl.sum_ad_should_display as PSD_LOG_ad_should_display,
    pl.sum_impression_Max    as PSD_LOG_Impression_Max
from creawler_table    ct
    inner join psd_log pl
               on ct.placement_name = pl.placement_name
                   and ct.bj_date = pl.bj_date
order by pl.bj_date,
         pl.placement_name
;



