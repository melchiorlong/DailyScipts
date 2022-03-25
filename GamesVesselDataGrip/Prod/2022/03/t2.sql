create table temp_country_ret_20220321_2_temp as
with date_set as (
    select distinct
        campaign_id,
        app_name,
        country,
        trunc(date) as ua_date
    from mid_dh_ua_new_data
    where 1 = 1
      and is_test = 'false'
      and to_char(date, 'YYYY-MM') = '2021-11'
)
select
    ds.campaign_id,
    rev_temp.app_name,
    rev_temp.ua_date,
    rev_temp.ua_country,
    dateadd(day, rev_temp.day_dimension, rev_temp.ua_date)        as action_date,
    sum(case when rev_temp.day_dimension = 1 then dau else 0 end) as sum_1_dau,
    sum(case when rev_temp.day_dimension = 7 then dau else 0 end) as sum_7_dau
from dws_ua_rev_dau_country_media_d rev_temp
    inner join date_set             ds
               on ds.app_name = rev_temp.app_name
                   and ds.country = rev_temp.ua_country
                   and ds.ua_date = rev_temp.ua_date
where 1 = 1
  and rev_temp.day_dimension in (1, 7)
  and ds.ua_date >= '2021-11-01'
group by rev_temp.ua_country,
         rev_temp.app_name,
         rev_temp.ua_date,
         rev_temp.day_dimension,
         dateadd(day, rev_temp.day_dimension, rev_temp.ua_date),
         ds.campaign_id
;



create table temp_single_detail_20220321_2 as
with date_set   as (
    select distinct
        app_name,
        country,
        optimizer,
        trunc(date) as date_str
    from mid_dh_ua_new_data
    where 1 = 1
      and is_test = 'false'
--       and optimizer = 'david'
--       and campaign_id = '23849245751420160'
      and to_char(date, 'YYYY-MM') = '2021-11'
),
     spend_temp as (
         select
             ds.date_str,
             ds.optimizer,
             ds.app_name,
             ds.country,
             spend_temp.ua_media,
             spend_temp.campaign_id,
             sum(spend) as sum_spend,
             sum(dnu)   as sum_dnu
         from dws_ua_spend_dnu_campaign_d spend_temp
             inner join date_set          ds
                        on ds.optimizer = spend_temp.optimizer
                            and ds.app_name = spend_temp.app_name
                            and ds.date_str = spend_temp.ua_date
                            and ds.country = spend_temp.ua_country
         where 1 = 1
           and spend > 0
--          and campaign_id = '23849245751420160'
           and ua_date >= '2021-11-01'
           and ua_date <= '2021-11-30'
         group by ds.optimizer,
                  ds.date_str,
                  ds.app_name,
                  ds.country,
                  spend_temp.campaign_id,
                  spend_temp.ua_media
     ),
     rev_temp   as (
         select
             ds.date_str,
             ds.optimizer,
             ds.app_name,
             ds.country,
             rev_temp.day_dimension,
             rev_temp.campaign_id,
             sum(case when day_dimension > 0 then dau else 0 end) as sum_dau,
             sum(rev)                                             as sum_rev
         from dws_ua_rev_dau_campaign_d rev_temp
             inner join date_set        ds
                        on ds.optimizer = rev_temp.optimizer
                            and ds.app_name = rev_temp.app_name
                            and ds.date_str = rev_temp.ua_date
                            and ds.country = rev_temp.ua_country
         where 1 = 1
           and day_dimension <= 90
           and ua_date >= '2021-11-01'
         group by ds.optimizer,
                  ds.date_str,
                  ds.app_name,
                  ds.country,
                  rev_temp.campaign_id,
                  rev_temp.day_dimension
     )
select
    st.campaign_id,
    st.date_str,
    nvl(rt.day_dimension, 0)                            as day_dimension,
    dateadd(day, nvl(rt.day_dimension, 0), st.date_str) as action_date,
    st.optimizer,
    st.app_name,
    st.country,
    st.ua_media,
    nvl(sum_rev, 0)                                     as single_rev,
    sum_spend                                           as single_spend,
    nvl(sum_dau, 0)                                     as single_dau,
    sum_dnu                                             as single_dnu
from spend_temp        st
    left join rev_temp rt
              on st.country = rt.country
                  and st.app_name = rt.app_name
                  and st.optimizer = rt.optimizer
                  and st.campaign_id = rt.campaign_id
                  and st.date_str = rt.date_str
;



with country_rev          as (
    select
        ua_country,
        app_name,
        ua_date,
        action_date,
        day_dimension,
        sum(country_rev)
        over (partition by ua_country, app_name, ua_date order by day_dimension rows between unbounded preceding and current row ) as agg_country_rev,
        sum(country_dau)
        over (partition by ua_country, app_name, ua_date order by day_dimension rows between unbounded preceding and current row ) as agg_country_dau,
        country_spend,
        country_dnu
    from temp_country_detail_20220321_2
),
     country_facebook_rev as (
         select
             ua_country,
             app_name,
             ua_date,
             action_date,
             day_dimension,
             sum(country_rev)
             over (partition by ua_country, app_name, ua_date order by day_dimension rows between unbounded preceding and current row ) as agg_country_rev,
             sum(country_dau)
             over (partition by ua_country, app_name, ua_date order by day_dimension rows between unbounded preceding and current row ) as agg_country_dau,
             country_spend,
             country_dnu
         from temp_country_facebook_detail_20220321_2
     ),
     single_rev           as (
         select
             country,
             app_name,
             date_str,
             action_date,
             optimizer,
             ua_media,
             day_dimension,
             sum(single_rev)
             over (partition by country, app_name, date_str order by day_dimension rows between unbounded preceding and current row ) as agg_single_rev,
             sum(single_dau)
             over (partition by country, app_name, date_str order by day_dimension rows between unbounded preceding and current row ) as agg_single_dau,
             single_spend,
             single_dnu
         from temp_single_detail_20220321_2
     )
select *
from single_rev
where campaign_id = '23849561746480560'
  and optimizer = 'dora'
;
,
     date_set             as (
         select distinct
             campaign_id,
             app_name,
             country,
             trunc(date) as ua_date
         from mid_dh_ua_new_data
         where 1 = 1
           and is_test = 'false'
           and to_char(date, 'YYYY-MM') = '2021-11'
     ),
     ds_temp              as (
         select
             ds.campaign_id,
             ds.app_name,
             ds.country,
             cr.action_date,
             sum(cr.agg_country_rev) as agg_country_rev,
             sum(cr.agg_country_dau) as agg_country_dau,
             sum(cr.country_spend)   as sum_country_spend,
             sum(cr.country_dnu)     as sum_country_dnu
         from date_set              ds
             inner join country_rev cr
                        on ds.country = cr.ua_country
                            and ds.app_name = cr.app_name
                            and ds.ua_date = cr.ua_date
         group by ds.campaign_id,
                  ds.app_name,
                  ds.country,
                  cr.action_date
     ),
     ds_facebook_temp     as (
         select
             ds.campaign_id,
             ds.app_name,
             ds.country,
             cr.action_date,
             sum(cr.agg_country_rev) as agg_country_rev,
             sum(cr.agg_country_dau) as agg_country_dau,
             sum(cr.country_spend)   as sum_country_spend,
             sum(cr.country_dnu)     as sum_country_dnu
         from date_set                       ds
             inner join country_facebook_rev cr
                        on ds.country = cr.ua_country
                            and ds.app_name = cr.app_name
                            and ds.ua_date = cr.ua_date
         group by ds.campaign_id,
                  ds.app_name,
                  ds.country,
                  cr.action_date
     ),
     ds_single_temp       as (
         select
             ds.campaign_id,
             ds.app_name,
             ds.country,
--              ds.ua_date             as date_str,
             cr.optimizer,
--              cr.day_dimension,
             cr.action_date,
             cr.ua_media,
             sum(cr.agg_single_rev) as single_rev,
             sum(cr.agg_single_dau) as single_dau,
             sum(cr.single_spend)   as single_spend,
             sum(cr.single_dnu)     as single_dnu
         from date_set             ds
             inner join single_rev cr
                        on ds.country = cr.country
                            and ds.app_name = cr.app_name
                            and ds.ua_date = cr.date_str
         group by ds.campaign_id,
                  ds.app_name,
                  ds.country,
                  cr.action_date,
                  cr.day_dimension,
                  ds.ua_date, cr.optimizer, cr.ua_media
     )
select
    sd.campaign_id,
--     sd.date_str,
--     sd.day_dimension,
    cd.action_date,
    sd.optimizer,
    sd.app_name,
    sd.country,
    sd.ua_media,
    sum(sd.single_rev)         as sum_single_rev,
    sum(sd.single_spend)       as sum_single_spend,
    sum(sd.single_dau)         as sum_single_dau,
    sum(sd.single_dnu)         as sum_single_dnu,
    max(cd.agg_country_rev)    as agg_country_rev,
    max(cd.agg_country_dau)    as agg_country_dau,
    sum(cd.sum_country_spend)  as sum_country_spend,
    sum(cd.sum_country_dnu)    as sum_country_dnu,
    sum(cfd.agg_country_rev)   as sum_country_facebook_rev,
    sum(cfd.agg_country_dau)   as sum_country_facebook_dau,
    sum(cfd.sum_country_spend) as sum_country_facebook_spend,
    sum(cfd.sum_country_dnu)   as sum_country_facebook_dnu,
    sum(cr.sum_1_dau)          as sum_1_dau,
    sum(cr.sum_7_dau)          as sum_7_dau
from ds_single_temp                       sd
    left join ds_temp                     cd
              on 1 = 1
                  and sd.campaign_id = cd.campaign_id


                  and cd.app_name = sd.app_name
                  and cd.country = sd.country
                  and cd.action_date = sd.action_date
    left join ds_facebook_temp            cfd
              on sd.campaign_id = cfd.campaign_id
                  and sd.app_name = cfd.app_name
                  and sd.country = cfd.country
                  and sd.action_date = cfd.action_date
    left join temp_country_ret_20220321_2 cr
              on cr.campaign_id = sd.campaign_id
                  and cr.app_name = sd.app_name
                  and cr.ua_country = sd.country
                  and cr.action_date = sd.action_date
where sd.campaign_id = '23849561746480560'
  and sd.optimizer = 'dora'
group by sd.campaign_id,
         sd.optimizer,
         sd.app_name,
         sd.country,
         sd.ua_media,
--          sd.date_str,
--          sd.day_dimension,
         cd.action_date
;

select *
from temp_single_detail_20220321_2
where campaign_id = '23849561746480560'


with country_spend as (
    select
        spend_temp.app_name,
        spend_temp.ua_date,
        spend_temp.ua_country,
        sum(spend) as sum_spend,
        sum(dnu)   as sum_dnu
    from dws_ua_spend_dnu_country_media_d spend_temp
    where 1 = 1
      and spend_temp.spend > 0
      and ua_date >= '2021-11-01'
      and ua_date <= '2021-11-30'
      and ua_media not in ('op_dohko', 'op_saori', 'Organic')
    group by spend_temp.ua_country,
             spend_temp.ua_date,
             spend_temp.app_name
),
     country_rev   as (
         select
             rev_temp.app_name,
             rev_temp.ua_date,
             rev_temp.ua_country,
             rev_temp.day_dimension,
             sum(case when rev_temp.day_dimension > 0 then dau else 0 end) as sum_dau,
             sum(rev)                                                      as sum_rev
         from dws_ua_rev_dau_country_media_d rev_temp
         where 1 = 1
           and day_dimension <= 90
           and ua_date >= '2021-11-01'
           and ua_media not in ('op_dohko', 'op_saori', 'Organic')
         group by rev_temp.ua_country,
                  rev_temp.app_name,
                  rev_temp.ua_date,
                  rev_temp.day_dimension
     ),
     temp          as (
         select
             cs.ua_date,
             cr.day_dimension,
             dateadd(day, cr.day_dimension, cs.ua_date) as action_date,
             cs.app_name,
             cs.ua_country,
             sum(sum_rev)                               as country_rev,
             sum(sum_spend)                             as country_spend,
             sum(sum_dau)                               as country_dau,
             sum(sum_dnu)                               as country_dnu
         from country_spend        cs
             left join country_rev cr
                       on cs.ua_date = cr.ua_date
                           and cs.app_name = cr.app_name
                           and cs.ua_country = cr.ua_country
         group by cs.ua_date,
                  cr.day_dimension,
                  cs.app_name,
                  cs.ua_country,
                  action_date
     )


select
    ua_country,
    app_name,
    ua_date,
    action_date,
    day_dimension,
    sum(country_rev)
    over (partition by ua_country, app_name, ua_date order by day_dimension rows between unbounded preceding and current row ) as agg_country_rev,
    sum(country_dau)
    over (partition by ua_country, app_name, ua_date order by day_dimension rows between unbounded preceding and current row ) as agg_country_dau,
    country_spend,
    country_dnu
from temp
where ua_country = 'GB'
  and app_name = 'saori_gp'
;



with country_rev          as (
    select
        ua_country,
        app_name,
        ua_date,
        action_date,
        day_dimension,
        sum(country_rev)
        over (partition by ua_country, app_name, ua_date order by day_dimension rows between unbounded preceding and current row ) as agg_country_rev,
        sum(country_dau)
        over (partition by ua_country, app_name, ua_date order by day_dimension rows between unbounded preceding and current row ) as agg_country_dau,
        country_spend,
        country_dnu
    from temp_country_detail_20220321_2
),
     country_facebook_rev as (
         select
             ua_country,
             app_name,
             ua_date,
             action_date,
             day_dimension,
             sum(country_rev)
             over (partition by ua_country, app_name, ua_date order by day_dimension rows between unbounded preceding and current row ) as agg_country_rev,
             sum(country_dau)
             over (partition by ua_country, app_name, ua_date order by day_dimension rows between unbounded preceding and current row ) as agg_country_dau,
             country_spend,
             country_dnu
         from temp_country_facebook_detail_20220321_2
     ),
     date_set             as (
         select distinct
             campaign_id,
             app_name,
             country,
             trunc(date) as ua_date
         from mid_dh_ua_new_data
         where 1 = 1
           and is_test = 'false'
           and to_char(date, 'YYYY-MM') = '2021-11'
     ),
     ds_temp              as (
         select
             ds.campaign_id,
             ds.app_name,
             ds.country,
             cr.action_date,
             sum(cr.agg_country_rev) as agg_country_rev,
             sum(cr.agg_country_dau) as agg_country_dau,
             max(cr.country_spend)   as sum_country_spend,
             max(cr.country_dnu)     as sum_country_dnu
         from date_set              ds
             inner join country_rev cr
                        on ds.country = cr.ua_country
                            and ds.app_name = cr.app_name
                            and ds.ua_date = cr.ua_date
         group by ds.campaign_id,
                  ds.app_name,
                  ds.country,
                  cr.action_date
     ),
     ds_facebook_temp     as (
         select
             ds.campaign_id,
             ds.app_name,
             ds.country,
             cr.action_date,
             sum(cr.agg_country_rev) as agg_country_rev,
             sum(cr.agg_country_dau) as agg_country_dau,
             max(cr.country_spend)   as sum_country_spend,
             max(cr.country_dnu)     as sum_country_dnu
         from date_set                       ds
             inner join country_facebook_rev cr
                        on ds.country = cr.ua_country
                            and ds.app_name = cr.app_name
                            and ds.ua_date = cr.ua_date
         group by ds.campaign_id,
                  ds.app_name,
                  ds.country,
                  cr.action_date
     ),
     temp                 as (
         select
             sd.campaign_id,
             sd.date_str,
             sd.day_dimension,
             cd.action_date,
             sd.optimizer,
             sd.app_name,
             sd.country,
             sd.ua_media,
             sum(sd.single_rev)         as sum_single_rev,
             sum(sd.single_spend)       as sum_single_spend,
             sum(sd.single_dau)         as sum_single_dau,
             sum(sd.single_dnu)         as sum_single_dnu,
             max(cd.agg_country_rev)    as agg_country_rev,
             max(cd.agg_country_dau)    as agg_country_dau,
             sum(cd.sum_country_spend)  as sum_country_spend,
             sum(cd.sum_country_dnu)    as sum_country_dnu,
             sum(cfd.agg_country_rev)   as sum_country_facebook_rev,
             sum(cfd.agg_country_dau)   as sum_country_facebook_dau,
             sum(cfd.sum_country_spend) as sum_country_facebook_spend,
             sum(cfd.sum_country_dnu)   as sum_country_facebook_dnu,
             sum(cr.sum_1_dau)          as sum_1_dau,
             sum(cr.sum_7_dau)          as sum_7_dau
         from temp_single_detail_20220321_2        sd
             left join ds_temp                     cd
                       on 1 = 1
                           and sd.campaign_id = cd.campaign_id
                           and cd.app_name = sd.app_name
                           and cd.country = sd.country
                           and cd.action_date = sd.action_date
             left join ds_facebook_temp            cfd
                       on sd.campaign_id = cfd.campaign_id
                           and sd.app_name = cfd.app_name
                           and sd.country = cfd.country
                           and sd.action_date = cfd.action_date
             left join temp_country_ret_20220321_2 cr
                       on cr.campaign_id = sd.campaign_id
                           and cr.app_name = sd.app_name
                           and cr.ua_country = sd.country
                           and cr.action_date = sd.action_date
         group by sd.campaign_id,
                  sd.optimizer,
                  sd.app_name,
                  sd.country,
                  sd.ua_media,
                  sd.date_str,
                  sd.day_dimension,
                  cd.action_date
     )
select *
from temp
where country = 'GB'
  and app_name = 'saori_gp'
  and campaign_id = '15277534077'
  and optimizer = 'serina'
;


