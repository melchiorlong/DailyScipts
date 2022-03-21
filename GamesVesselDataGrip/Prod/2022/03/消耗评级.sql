-- 计算这些 DNU【至今】的留存LT 和 ROI
with date_set                as (
    select distinct
        app_name,
        country,
        optimizer,
        trunc(date) as date_str
    from mid_dh_ua_new_data
    where 1 = 1
      and is_test = 'false'
--       and optimizer = 'david'
      and to_char(date, 'YYYY-MM') = '2021-11'
),
     country_ret             as (
         select
             rev_temp.app_name,
             rev_temp.ua_date,
             rev_temp.ua_country,
             sum(case when rev_temp.day_dimension = 1 then dau else 0 end) as sum_1_dau,
             sum(case when rev_temp.day_dimension = 7 then dau else 0 end) as sum_7_dau
         from dws_ua_rev_dau_country_media_d rev_temp
         where 1 = 1
--            and day_dimension in (1, 7)
         group by rev_temp.ua_country,
                  rev_temp.app_name,
                  rev_temp.ua_date
     ),
     country_spend           as (
         select
             spend_temp.app_name,
             spend_temp.ua_date,
             spend_temp.ua_country,
             spend_temp.ua_media,
             sum(spend) as sum_spend,
             sum(dnu)   as sum_dnu
         from dws_ua_spend_dnu_country_media_d spend_temp
         where spend_temp.spend > 0
           and ua_media not in ('op_dohko', 'op_saori', 'Organic')
         group by spend_temp.ua_country,
                  spend_temp.ua_date,
                  spend_temp.app_name,
                  spend_temp.ua_media
     ),
     country_rev             as (
         select
             rev_temp.app_name,
             rev_temp.ua_date,
             rev_temp.ua_country,
             rev_temp.ua_media,
             sum(case when rev_temp.day_dimension > 0 then dau else 0 end) as sum_dau,
             sum(rev)                                                      as sum_rev
         from dws_ua_rev_dau_country_media_d rev_temp
         where 1 = 1
           and day_dimension <= 90
           and ua_media not in ('op_dohko', 'op_saori', 'Organic')
         group by rev_temp.ua_country,
                  rev_temp.app_name,
                  rev_temp.ua_date,
                  rev_temp.ua_media
     ),
     country_facebook_spend  as (
         select
             spend_temp.app_name,
             spend_temp.ua_date,
             spend_temp.ua_country,
             sum(spend) as sum_spend,
             sum(dnu)   as sum_dnu
         from dws_ua_spend_dnu_country_media_d spend_temp
         where spend_temp.spend > 0
           and ua_media = 'Facebook'
         group by spend_temp.ua_country,
                  spend_temp.ua_date,
                  spend_temp.app_name
     ),
     country_facebok_rev     as (
         select
             rev_temp.app_name,
             rev_temp.ua_date,
             rev_temp.ua_country,
             sum(case when rev_temp.day_dimension > 0 then dau else 0 end) as sum_dau,
             sum(rev)                                                      as sum_rev
         from dws_ua_rev_dau_country_media_d rev_temp
         where 1 = 1
           and rev_temp.day_dimension <= 90
           and rev_temp.ua_media = 'Facebook'
         group by rev_temp.ua_country,
                  rev_temp.app_name,
                  rev_temp.ua_date
     ),
     country_facebook_detail as (
         select
             cr.ua_date,
             cr.app_name,
             cr.ua_country,
             sum_rev   as country_rev,
             sum_spend as country_spend,
             sum_dau   as country_dau,
             sum_dnu   as country_dnu
         from country_facebook_spend        cs
             inner join country_facebok_rev cr
                        on cs.ua_date = cr.ua_date
                            and cs.app_name = cr.app_name
                            and cs.ua_country = cr.ua_country
     ),
     country_detail          as (
         select
             cr.ua_date,
             cr.app_name,
             cr.ua_country,
             sum(sum_rev)   as country_rev,
             sum(sum_spend) as country_spend,
             sum(sum_dau)   as country_dau,
             sum(sum_dnu)   as country_dnu
         from country_spend         cs
             inner join country_rev cr
                        on cs.ua_date = cr.ua_date
                            and cs.app_name = cr.app_name
                            and cs.ua_country = cr.ua_country
                            and cs.ua_media = cr.ua_media
         group by cr.ua_date,
                  cr.app_name,
                  cr.ua_country
     ),
     spend_temp              as (
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

--          and campaign_id = '23849952411650710'

         group by ds.optimizer,
                  ds.date_str,
                  ds.app_name,
                  ds.country,
                  spend_temp.campaign_id,
                  spend_temp.ua_media
     )

--      select * from spend_temp;
        ,
     rev_temp                as (
         select
             ds.date_str,
             ds.optimizer,
             ds.app_name,
             ds.country,
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
         group by ds.optimizer,
                  ds.date_str,
                  ds.app_name,
                  ds.country,
                  rev_temp.campaign_id
     )
--      select * from rev_temp;
        ,
     single_detail           as (
         select
             st.date_str,
             st.campaign_id,
             st.optimizer,
             st.app_name,
             st.country,
             st.ua_media,
             sum_rev   as single_rev,
             sum_spend as single_spend,
             sum_dau   as single_dau,
             sum_dnu   as single_dnu
         from spend_temp        st
             left join rev_temp rt
                       on st.country = rt.country
                           and st.app_name = rt.app_name
                           and st.optimizer = rt.optimizer
                           and st.campaign_id = rt.campaign_id
                           and st.date_str = rt.date_str
     )
--      select * from single_detail;
        ,
     combine_temp            as (
         select
             sd.campaign_id,
             sd.optimizer,
             sd.app_name,
             sd.country,
             sd.ua_media,
             sum(sd.single_rev)     as sum_single_rev,
             sum(sd.single_spend)   as sum_single_spend,
             sum(sd.single_dau)     as sum_single_dau,
             sum(sd.single_dnu)     as sum_single_dnu,
             sum(cd.country_rev)    as sum_country_rev,
             sum(cd.country_spend)  as sum_country_spend,
             sum(cd.country_dau)    as sum_country_dau,
             sum(cd.country_dnu)    as sum_country_dnu,

             sum(cfd.country_rev)   as sum_country_facebook_rev,
             sum(cfd.country_spend) as sum_country_facebook_spend,
             sum(cfd.country_dau)   as sum_country_facebook_dau,
             sum(cfd.country_dnu)   as sum_country_facebook_dnu,

             sum(cr.sum_1_dau)      as sum_1_dau,
             sum(cr.sum_7_dau)      as sum_7_dau
         from single_detail                     sd
             inner join country_detail          cd
                        on cd.ua_date = sd.date_str
                            and cd.app_name = sd.app_name
                            and cd.ua_country = sd.country
             left join  country_facebook_detail cfd
                        on sd.date_str = cfd.ua_date
                            and sd.app_name = cfd.app_name
                            and sd.country = cfd.ua_country
             left join  country_ret             cr
                        on cr.ua_date = sd.date_str
                            and cr.app_name = sd.app_name
                            and cr.ua_country = sd.country
         group by sd.campaign_id,
                  sd.optimizer,
                  sd.app_name,
                  sd.country,
                  sd.ua_media
     )
--      select * from combine_temp;
        ,
     combine_temp_table      as (
         select *,
                1.0 * sum_single_rev / sum_single_spend                                 as single_roi,
                1 + (1.0 * sum_single_dau / sum_single_dnu)                             as single_lt,
                1.0 * sum_country_rev / sum_country_spend                               as country_roi,
                1 + (1.0 * sum_country_dau / sum_country_dnu)                           as country_lt,
                nvl(1.0 * sum_country_facebook_rev / sum_country_facebook_spend, 0)     as country_facebook_roi,
                nvl(1 + (1.0 * sum_country_facebook_dau / sum_country_facebook_dnu), 0) as country_facebook_lt,
                case when single_roi > country_roi then 1 else 0 end                    as single_roi_great_country,
                case when single_lt > country_lt then 1 else 0 end                      as single_lt_great_country,
                case when country_facebook_roi > country_roi then 1 else 0 end          as facebook_roi_great_country,
                case when country_facebook_lt > country_lt then 1 else 0 end            as facebook_lt_great_country,
                case
                    when sum_7_dau > 0
                        then 1.0 * sum_1_dau / sum_7_dau
                    when sum_7_dau = 0
                        then 9999
                        else null
                    end                                                                 as country_ret,
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
                    end                                                                 as rating_rule,
                split_part(rating_rule, '_', 1)                                         as rate,
                split_part(rating_rule, '_', 2)                                         as rule
         from combine_temp
     )
select
    campaign_id,
    optimizer,
    app_name,
    country,
    ua_media,
    rate,
    rule,
    sum(sum_single_spend) over (partition by optimizer, rate) /
    sum(sum_single_spend) over (partition by optimizer) as rate_percent,
    sum_single_rev,
    sum_single_spend,
    sum_single_dau,
    sum_single_dnu,
    sum_country_rev,
    sum_country_spend,
    sum_country_dau,
    sum_country_dnu,
    sum_country_facebook_rev,
    sum_country_facebook_spend,
    sum_country_facebook_dau,
    sum_country_facebook_dnu,
    sum_1_dau,
    sum_7_dau,
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