select
    rev_temp.app_name,
    rev_temp.ua_date,
    rev_temp.ua_country,
    sum(case when rev_temp.day_dimension = 1 then dau else 0 end) as sum_1_dau,
    sum(case when rev_temp.day_dimension = 7 then dau else 0 end) as sum_7_dau
from dws_ua_rev_dau_country_media_d rev_temp
where 1 = 1
--            and day_dimension in (1, 7)
  and ua_country = 'US'
  and app_name = 'saori_gp'
  and ua_date in (
    select distinct
        trunc(date) as date_str
    from mid_dh_ua_new_data
    where 1 = 1
      and campaign_id = '23850097736090767'
      and country = 'US'
      and app_name = 'saori_gp'
--       and is_test = 'false'
--       and optimizer = 'david'
      and to_char(date, 'YYYY-MM') = '2022-01'
)
group by rev_temp.ua_country,
         rev_temp.app_name,
         rev_temp.ua_date




select
distinct ua_media
from dws_ua_spend_dnu_country_media_d;


select
distinct ua_media
from dws_ua_rev_dau_country_media_d;



select
distinct *
from mid_dh_ua_new_data
where 1=1
and campaign_id = '23849559698140602'
and optimizer = 'nancy'
and to_char(date, 'YYYY-MM') = '2022-01'