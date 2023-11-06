import re
from sqllineage.runner import LineageRunner

# Replace with your actual SQL query
sql = """
with creawler_table as (    
    select        
        placement_name,        
        sum(impr) as sum_impr    
    from mid_dh_market_data    
    where app_name = 'saori_ip'    
    group by placement_name, bj_date
),     
psd_log as (         
    select             
        placement_name,             
        sum(case when action_type = 'impression' then 1 else 0 end) as sum_impr,
        sum(case when action_type = 'ad_should_display' then 1 else 0 end) as sum_ad_should_display,
        sum(case when action_type = 'impression' and app_version_code > 28 then 1 else 0 end) as sum_impression_Max         
    from spectrum.fact_ivt_poseidon_log log         
    where 1 = 1           
    and action_type in ('impression', 'ad_should_display')           
    and app_package_name = 'art.color.planet.paint.by.number.game.puzzle'         
    group by bj_date, placement_name     
)
select    
    pl.bj_date,    
    pl.placement_name,    
    ct.sum_impr as CrawlerTask_Impression,
    pl.sum_impr as PSD_LOG_Impression,
    pl.sum_ad_should_display as PSD_LOG_ad_should_display,
    pl.sum_impression_Max as PSD_LOG_Impression_Max
from creawler_table ct    
inner join psd_log pl on ct.placement_name = pl.placement_name and ct.bj_date = pl.bj_date
order by pl.bj_date, pl.placement_name;
"""

res = LineageRunner(sql)
cols = res.get_column_lineage(exclude_subquery=False)

for fac in cols:
    print(fac)



