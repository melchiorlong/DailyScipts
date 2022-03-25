drop table if exists temp_country_facebook_detail_20220321_2;
drop table if exists temp_country_ret_20220321_2;
drop table if exists temp_single_detail_20220321_2;
drop table if exists temp_country_detail_20220321_2;

drop table if exists temp_combine_20220321_2;
drop table if exists temp_aggr_combine_20220321_2;

drop table if exists temp_aggr_action_date_20220321;
drop table if exists temp_combine_temp_table_20220321;



create table temp_country_facebook_detail_20220321_2 as
with country_facebook_spend as (
    select
        spend_temp.app_name,
        spend_temp.ua_date,
        spend_temp.ua_country,
        sum(spend) as sum_spend,
        sum(dnu)   as sum_dnu
    from dws_ua_spend_dnu_country_media_d spend_temp
    where spend_temp.spend > 0
      and ua_media = 'Facebook'
      and ua_date >= '2021-11-01'
      and ua_date <= '2021-11-30'
    group by spend_temp.ua_country,
             spend_temp.ua_date,
             spend_temp.app_name
),
     country_facebok_rev    as (
         select
             rev_temp.app_name,
             rev_temp.ua_date,
             rev_temp.ua_country,
             rev_temp.day_dimension,
             sum(case when rev_temp.day_dimension > 0 then dau else 0 end) as sum_dau,
             sum(rev)                                                      as sum_rev
         from dws_ua_rev_dau_country_media_d rev_temp
         where 1 = 1
           and rev_temp.day_dimension <= 90
           and ua_date >= '2021-11-01'
           and rev_temp.ua_media = 'Facebook'
         group by rev_temp.ua_country,
                  rev_temp.app_name,
                  rev_temp.ua_date,
                  rev_temp.day_dimension
     )
select
    cs.ua_date,
    cr.day_dimension,
    cr.app_name,
    cr.ua_country,
    dateadd(day, cr.day_dimension, cs.ua_date) as action_date,
    sum_rev                                    as country_rev,
    sum_spend                                  as country_spend,
    sum_dau                                    as country_dau,
    sum_dnu                                    as country_dnu
from country_facebook_spend        cs
    inner join country_facebok_rev cr
               on cs.ua_date = cr.ua_date
                   and cs.app_name = cr.app_name
                   and cs.ua_country = cr.ua_country
;


create table temp_country_ret_20220321_2 as
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

select *
from temp_country_ret_20220321_2
order by ua_date,
         ua_country,
         app_name
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


select *
from temp_single_detail_20220321_2
where 1 = 1
  and campaign_id = '612b7e745a271f7b0f78d76a'
  and country = 'US'
  and optimizer = 'jimmy';



create table temp_country_detail_20220321_2 as
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
     )
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
;



select
    action_date,
    sum(country_rev)
from temp_country_detail_20220321_2
where ua_country = 'US'
  and app_name = 'aiolos_gp'
  and action_date <= '2022-12-15'
  and ua_date in (
    select distinct
        date
    from mid_dh_ua_new_data
    where 1 = 1
      and campaign_id = '15277534077'
      and country = 'GB'
      and optimizer = 'serina'
      and date >= '2021-11-01'
      and date <= '2021-11-30'
)
group by action_date;


create table temp_combine_20220321_2 as
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
     )
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
;



select
    dateadd(day, day_dimension, date_str) as action_date,
    *
from temp_combine_20220321_2
where 1 = 1
  and campaign_id = '15277534077'
  and country = 'GB'
  and optimizer = 'serina'
order by campaign_id,
         app_name,
         optimizer,
         date_str,
         day_dimension
;


create table temp_aggr_combine_20220321_2 as
select
    campaign_id,
    date_str,
    day_dimension,
    optimizer,
    app_name,
    country,
    ua_media,

    sum(sum_single_rev)
    over (partition by campaign_id, optimizer, app_name, country, ua_media order by day_dimension rows between unbounded preceding and current row ) as agg_single_rev,
    sum_single_spend                                                                                                                                 as single_spend,
    sum(sum_single_dau)
    over (partition by campaign_id, optimizer, app_name, country, ua_media order by day_dimension rows between unbounded preceding and current row ) as agg_single_dau,
    sum_single_dnu                                                                                                                                   as single_dnu,

    agg_country_rev                                                                                                                                  as country_rev,
    agg_country_dau                                                                                                                                  as country_dau,
    sum_country_spend                                                                                                                                as country_spend,
    sum_country_dnu                                                                                                                                  as country_dnu,

    sum_country_facebook_rev                                                                                                                         as country_facebook_rev,
    sum_country_facebook_dau                                                                                                                         as country_facebook_dau,
    sum_country_facebook_spend                                                                                                                       as country_facebook_spend,
    sum_country_facebook_dnu                                                                                                                         as country_facebook_dnu,

    sum(sum_1_dau)
    over (partition by campaign_id, optimizer, app_name, country, ua_media order by day_dimension rows between unbounded preceding and current row ) as agg_1_dau,
    sum(sum_7_dau)
    over (partition by campaign_id, optimizer, app_name, country, ua_media order by day_dimension rows between unbounded preceding and current row ) as agg_7_dau
from temp_combine_20220321_2
;

select
    dateadd(day, day_dimension, date_str),
    *
from temp_aggr_combine_20220321_2
where campaign_id = '23849561746480560';



create table temp_aggr_action_date_20220321 as
with row_numer_temp as (
    select *
    from (
        select *,
               row_number()
               over (partition by campaign_id,optimizer,date_str,app_name, country,ua_media order by day_dimension) as rn
        from temp_aggr_combine_20220321_2
    ) temp_table
    where temp_table.rn = 1
),
     spend_temp     as (
         select
             campaign_id,
             optimizer,
             app_name,
             country,
             ua_media,
             sum(single_spend) as sum_single_spend,
             sum(single_dnu)   as sum_single_dnu
         from row_numer_temp
         group by campaign_id,
                  optimizer,
                  app_name,
                  country,
                  ua_media
     )
select
    tac.campaign_id,
    tac.date_str,
    dateadd(day, day_dimension, date_str) as action_date,
    tac.optimizer,
    tac.app_name,
    tac.country,
    tac.ua_media,
    sum(tac.agg_single_rev)               as agg_single_rev,
    sum(st.sum_single_spend)              as single_spend,
    sum(tac.agg_single_dau)               as agg_single_dau,
    sum(st.sum_single_dnu)                as single_dnu,
    max(tac.country_rev)                  as agg_country_rev,
    max(tac.country_spend)                as country_spend,
    max(tac.country_dau)                  as agg_country_dau,
    max(tac.country_dnu)                  as country_dnu,
    max(tac.country_facebook_rev)         as agg_country_fb_rev,
    max(tac.country_facebook_spend)       as country_fb_spend,
    max(tac.country_facebook_dau)         as agg_country_fb_dau,
    max(tac.country_facebook_dnu)         as sum_country_facebook_dnu,
    sum(tac.agg_1_dau)                    as agg_1_dau,
    sum(tac.agg_7_dau)                    as agg_7_dau
from spend_temp                             st
    inner join temp_aggr_combine_20220321_2 tac
               on st.ua_media = tac.ua_media
                   and st.campaign_id = tac.campaign_id
                   and st.optimizer = tac.optimizer
                   and st.app_name = tac.app_name
                   and st.country = tac.country
where st.campaign_id = '23849561746480560'
group by tac.campaign_id,
         tac.date_str,
         dateadd(day, day_dimension, date_str),
         tac.optimizer,
         tac.app_name,
         tac.country,
         tac.ua_media
;



select *
from temp_aggr_action_date_20220321
where 1 = 1
  and campaign_id = '612b7e745a271f7b0f78d76a'
  and country = 'US'
  and optimizer = 'jimmy';

create table temp_combine_temp_table_20220321 as
with combine_temp_table as (
    select *,
           case
               when single_spend > 0
                   then 1.0 * agg_single_rev / single_spend
                   else null end                                                              as single_roi,
           case
               when agg_single_dau > 0
                   then 1 + (1.0 * agg_single_dau / agg_single_dau)
                   else null end                                                              as single_lt,
           case
               when country_spend > 0
                   then 1.0 * agg_country_rev / country_spend
                   else null end                                                              as country_roi,
           case when country_dnu > 0 then 1 + (1.0 * agg_country_dau / country_dnu) end       as country_lt,
           case
               when country_fb_spend > 0
                   then nvl(1.0 * agg_country_fb_rev / country_fb_spend, 0) end               as country_facebook_roi,
           case
               when sum_country_facebook_dnu > 0
                   then nvl(1 + (1.0 * agg_country_fb_dau / sum_country_facebook_dnu), 0) end as country_facebook_lt,
           case when single_roi > country_roi then 1 else 0 end                               as single_roi_great_country,
           case when single_lt > country_lt then 1 else 0 end                                 as single_lt_great_country,
           case when country_facebook_roi > country_roi then 1 else 0 end                     as facebook_roi_great_country,
           case when country_facebook_lt > country_lt then 1 else 0 end                       as facebook_lt_great_country,
           case
               when agg_7_dau > 0
                   then 1.0 * agg_1_dau / agg_7_dau
               when agg_7_dau = 0
                   then 9999
                   else null
               end                                                                            as country_ret,
           case
               -- Android and Not Facebook
               when ua_media <> 'Facebook' and right(app_name, 2) = 'gp'
                   and single_roi_great_country + single_lt_great_country = 2
                   then 'A_1.1'
               when ua_media <> 'Facebook' and right(app_name, 2) = 'gp'
                   and single_lt_great_country = 1
                   and single_roi_great_country = 0
                   then 'C_1.2'
               when ua_media <> 'Facebook' and right(app_name, 2) = 'gp'
                   and single_lt_great_country = 0
                   and single_roi_great_country = 1
                   then 'C_1.3'
               when ua_media <> 'Facebook' and right(app_name, 2) = 'gp'
                   and single_roi_great_country + single_lt_great_country = 0
                   then 'D_1.4'
               -- Android and Facebook
               when ua_media = 'Facebook' and right(app_name, 2) = 'gp'
                   and single_roi_great_country + single_lt_great_country = 2
                   then 'A_2.1'
               when ua_media = 'Facebook' and right(app_name, 2) = 'gp'
                   and single_lt_great_country = 1
                   and single_roi_great_country = 0
                   and facebook_roi_great_country = 1
                   then 'B_2.2'
               when ua_media = 'Facebook' and right(app_name, 2) = 'gp'
                   and single_lt_great_country = 1
                   and single_roi_great_country = 0
                   and facebook_roi_great_country = 0
                   then 'C_2.3'
               when ua_media = 'Facebook' and right(app_name, 2) = 'gp'
                   and
                    (
                                single_lt_great_country = 0 and
                                (single_roi_great_country = 1 or facebook_roi_great_country = 0)
                        )
                   then 'C_2.4'
               when ua_media = 'Facebook' and right(app_name, 2) = 'gp'
                   and single_roi_great_country + single_lt_great_country = 0
                   then 'D_2.5'


               -- iOS and Search Ads
               when ua_media = 'Apple Search Ads' and right(app_name, 2) = 'ip'
                   and single_roi_great_country + single_lt_great_country = 2
                   then 'A_3.1'
               when ua_media = 'Apple Search Ads' and right(app_name, 2) = 'ip'
                   and single_lt_great_country = 1
                   and single_roi_great_country = 0
                   then 'C_3.2'
               when ua_media = 'Apple Search Ads' and right(app_name, 2) = 'ip'
                   and single_lt_great_country = 0
                   and single_roi_great_country = 1
                   then 'C_3.3'
               when ua_media = 'Apple Search Ads' and right(app_name, 2) = 'ip'
                   and single_roi_great_country + single_lt_great_country = 0
                   then 'D_3.4'
               -- iOS and Not Search Ads
               when ua_media <> 'Apple Search Ads' and right(app_name, 2) = 'ip' and country_ret is null
                   then 'RetNotEnough_RetNotEnough'
               when ua_media <> 'Apple Search Ads' and right(app_name, 2) = 'ip'
                   and country_ret <= 2
                   then 'A_4.1'
               when ua_media <> 'Apple Search Ads' and right(app_name, 2) = 'ip'
                   and country_ret > 2
                   and country_ret <= 2.25
                   then 'B_4.2'
               when ua_media <> 'Apple Search Ads' and right(app_name, 2) = 'ip'
                   and country_ret > 2.25
                   and country_ret <= 2.5
                   then 'C_4.3'
               when ua_media <> 'Apple Search Ads' and right(app_name, 2) = 'ip'
                   and country_ret > 2.5
                   then 'D_4.4'
                   else 'Unknown'
               end                                                                            as rating_rule,
           split_part(rating_rule, '_', 1)                                                    as rate,
           split_part(rating_rule, '_', 2)                                                    as rule
    from temp_aggr_action_date_20220321
)
select
    campaign_id,
    action_date,
    optimizer,
    app_name,
    country,
    ua_media,
    rate,
    rule,
    sum(single_spend) over (partition by optimizer, rate) /
    sum(single_spend) over (partition by optimizer) as rate_percent,
    agg_single_rev,
    single_spend,
    agg_single_dau,
    single_dnu,
    agg_country_rev,
    country_spend,
    agg_country_dau,
    country_dnu,
    agg_country_fb_rev,
    country_fb_spend,
    agg_country_fb_dau,
    sum_country_facebook_dnu,
    agg_1_dau,
    agg_7_dau,
    single_roi,
    single_lt,
    country_roi,
    country_lt,
    country_facebook_roi,
    country_facebook_lt,
    single_roi_great_country,
    single_lt_great_country,
    facebook_roi_great_country,
    facebook_lt_great_country,
    country_ret
from combine_temp_table
where 1 = 1
--   and optimizer = 'sherry'
--   and campaign_id = '23848855579080757';
order by optimizer,
         app_name,
         ua_media,
         country
;


select *
from temp_combine_temp_table_20220321
where 1 = 1
  and campaign_id = '15277534077'
  and country = 'GB'
  and optimizer = 'serina'
--   and action_date = '2022-01-10'
order by campaign_id,
         optimizer,
         app_name,
         country,
         ua_media
-- limit 500
;



select *
from dws_ua_rev_dau_country_media_d
where 1 = 1
  and app_name = 'saori_gp'
  and ua_country = 'GB'
  and ua_date in (
    select distinct
        ua_date
    from mid_dh_ua_new_data
    where campaign_id = '15277534077'
      and country = 'GB'
      and optimizer = 'serina'
      and ua_date >= '2021-11-01'
      and ua_date <= '2021-11-30'
);

select *
from dws_ua_spend_dnu_country_media_d
where 1 = 1
  and app_name = 'saori_gp'
  and ua_country = 'GB'
  and ua_date in (
    select distinct
        date
    from mid_dh_ua_new_data
    where campaign_id = '15277534077'
      and is_test = 'false'
      and country = 'GB'
      and optimizer = 'serina'
      and date >= '2021-11-01'
      and date <= '2021-11-30'
)


