with tmp_split_country_campaign_info as (
    select
        dh.date,
        dh.campaign_id,
        info.campaign_name,
        dh.media_source                                  as ua_media,
        dh.app_name,
        datediff(days, info.campaign_birthdate, sysdate) as campaign_living_days,
        dh.country,
        sum(dh.spend)                                    as spend,
        nvl(sum(dh.installs), 0)                         as installs,
        nvl(sum(dh.clicks), 0)                           as clicks,
        nvl(sum(dh.impressions), 0)                      as impressions
    from dim_poseidon_campaign_info as info
        inner join
    mid_dh_ua_data                  as dh
    on
        dh.campaign_id = info.campaign_id
    where info.source = 'dh'         -- 来源于dh表的campaign
      and dh.date >= '2022-03-28'
      and dh.date <= '2022-04-10'
      and info.campaign_app_name = 'aiolos_gp' and dh.app_name = 'aiolos_gp' and info.campaign_media_source = 'Google'
      and dh.media_source = 'Google' -- 注意这里不能够进行国家过滤，否则后面拿不到campaign实际花费的国家数目

    group by dh.date,
             dh.campaign_id,
             info.campaign_name,
             dh.media_source,
             dh.app_name,
             info.campaign_birthdate,
             dh.country
),
     tmp_agg_country_str             as (
         select
             campaign_id,
             listagg(DISTINCT country, '|') as country_str
         from tmp_split_country_campaign_info
         group by campaign_id
     ),
     tmp_campaign_attribute          as ( -- campaign固有属性，每个campaign id应该只有一个才对
         select
             info.campaign_id,
             campaign_name,
             ua_media,
             app_name,
             campaign_living_days,
             tacs.country_str
         from tmp_split_country_campaign_info as info
             left join
         tmp_agg_country_str                  as tacs
         on
             info.campaign_id = tacs.campaign_id
         group by info.campaign_id,
                  campaign_name,
                  ua_media,
                  app_name,
                  campaign_living_days,
                  tacs.country_str
     ),
     tmp_all_dh_install_info         as (
         select
             dh.campaign_id,
             dh.date,
             sum(installs) as all_country_dh_installs
         from tmp_split_country_campaign_info as dh
         where dh.date >= '2022-03-28'
           and dh.date <= '2022-04-10'
         group by dh.campaign_id,
                  dh.date
     ),
     tmp_agg_country_campaign_info   as (
         select
             date,
             campaign_id,
             nvl(sum(spend), 0.0)     as spend,
             nvl(sum(installs), 0)    as installs,
             nvl(sum(clicks), 0)      as clicks,
             nvl(sum(impressions), 0) as impressions
         from tmp_split_country_campaign_info
         where 1 = 1
           and country = 'CA' -- 这里进行国家数据的过滤
         group by date,
                  campaign_id
     ),
     tmp_campaign_id                 as (
         select distinct
             (campaign_id) as campaign_id
         from tmp_agg_country_campaign_info
     ),
     campaign_rev                    as (
         select
             campaign_id,
             bj_date                                                                    as date,
             nvl(sum(day0_ads_rev), 0.0)                                                as day0_ads_rev,
             nvl(sum(day0_iap_rev), 0.0)                                                as day0_iap_rev,
             nvl(max(case when day0_ads_rev_include_fb = 'true' then 1 else 0 end), 0)  as day0_ads_rev_include_fb,
             nvl(sum(day1_ads_rev), 0.0)                                                as day1_ads_rev,
             nvl(sum(day1_iap_rev), 0.0)                                                as day1_iap_rev,
             nvl(max(case when day1_ads_rev_include_fb = 'true' then 1 else 0 end), 0)  as day1_ads_rev_include_fb,
             nvl(sum(day2_ads_rev), 0.0)                                                as day2_ads_rev,
             nvl(sum(day2_iap_rev), 0.0)                                                as day2_iap_rev,
             nvl(max(case when day2_ads_rev_include_fb = 'true' then 1 else 0 end), 0)  as day2_ads_rev_include_fb,
             nvl(sum(day3_ads_rev), 0.0)                                                as day3_ads_rev,
             nvl(sum(day3_iap_rev), 0.0)                                                as day3_iap_rev,
             nvl(max(case when day3_ads_rev_include_fb = 'true' then 1 else 0 end), 0)  as day3_ads_rev_include_fb,
             nvl(sum(day7_ads_rev), 0.0)                                                as day7_ads_rev,
             nvl(sum(day7_iap_rev), 0.0)                                                as day7_iap_rev,
             nvl(max(case when day7_ads_rev_include_fb = 'true' then 1 else 0 end), 0)  as day7_ads_rev_include_fb,
             nvl(sum(day14_ads_rev), 0.0)                                               as day14_ads_rev,
             nvl(sum(day14_iap_rev), 0.0)                                               as day14_iap_rev,
             nvl(max(case when day14_ads_rev_include_fb = 'true' then 1 else 0 end), 0) as day14_ads_rev_include_fb,
             nvl(sum(day30_ads_rev), 0.0)                                               as day30_ads_rev,
             nvl(sum(day30_iap_rev), 0.0)                                               as day30_iap_rev,
             nvl(max(case when day30_ads_rev_include_fb = 'true' then 1 else 0 end), 0) as day30_ads_rev_include_fb
         from mid_ilrd_campaign_roi_total_rev
         where bj_date >= '2022-03-28'
           and bj_date <= '2022-04-10'
           and campaign_id in (
             select
                 campaign_id
             from tmp_campaign_id
         )
           and country = 'CA' -- 收入可能需要基于国家过滤
         group by bj_date,
                  campaign_id
     ),
     campaign_rs                     as (
         select
             info.date,
             info.campaign_id,
             info.spend,
             info.installs,
             info.clicks,
             info.impressions,
             nvl(day0_ads_rev, 0.0)           as day0_ads_rev,
             nvl(day0_iap_rev, 0.0)           as day0_iap_rev,
             nvl(day0_ads_rev_include_fb, 0)  as day0_ads_rev_include_fb,
             nvl(day1_ads_rev, 0.0)           as day1_ads_rev,
             nvl(day1_iap_rev, 0.0)           as day1_iap_rev,
             nvl(day1_ads_rev_include_fb, 0)  as day1_ads_rev_include_fb,
             nvl(day2_ads_rev, 0.0)           as day2_ads_rev,
             nvl(day2_iap_rev, 0.0)           as day2_iap_rev,
             nvl(day2_ads_rev_include_fb, 0)  as day2_ads_rev_include_fb,
             nvl(day3_ads_rev, 0.0)           as day3_ads_rev,
             nvl(day3_iap_rev, 0.0)           as day3_iap_rev,
             nvl(day3_ads_rev_include_fb, 0)  as day3_ads_rev_include_fb,
             nvl(day7_ads_rev, 0.0)           as day7_ads_rev,
             nvl(day7_iap_rev, 0.0)           as day7_iap_rev,
             nvl(day7_ads_rev_include_fb, 0)  as day7_ads_rev_include_fb,
             nvl(day14_ads_rev, 0.0)          as day14_ads_rev,
             nvl(day14_iap_rev, 0.0)          as day14_iap_rev,
             nvl(day14_ads_rev_include_fb, 0) as day14_ads_rev_include_fb,
             nvl(day30_ads_rev, 0.0)          as day30_ads_rev,
             nvl(day30_iap_rev, 0.0)          as day30_iap_rev,
             nvl(day30_ads_rev_include_fb, 0) as day30_ads_rev_include_fb
         from tmp_agg_country_campaign_info as info
             left join campaign_rev         as rev
                       on info.date = rev.date
                           and info.campaign_id = rev.campaign_id
     ),
     all_country_retention_info      as (
         select
             campaign_id,
             to_timestamp(bj_date, 'YYYY-MM-DD')   as date,
             country,
             nvl(sum(install_count), 0)            as install,
             nvl(sum(install_muid_count), 0)       as muid_install,
             nvl(sum(retention_1d_count), 0)       as retention_1d_count,
             nvl(sum(retention_1d_muid_count), 0)  as retention_1d_muid_count,
             nvl(sum(retention_2d_count), 0)       as retention_2d_count,
             nvl(sum(retention_2d_muid_count), 0)  as retention_2d_muid_count,
             nvl(sum(retention_3d_count), 0)       as retention_3d_count,
             nvl(sum(retention_3d_muid_count), 0)  as retention_3d_muid_count,
             nvl(sum(retention_7d_count), 0)       as retention_7d_count,
             nvl(sum(retention_7d_muid_count), 0)  as retention_7d_muid_count,
             nvl(sum(retention_14d_count), 0)      as retention_14d_count,
             nvl(sum(retention_14d_muid_count), 0) as retention_14d_muid_count,
             nvl(sum(retention_30d_count), 0)      as retention_30d_count,
             nvl(sum(retention_30d_muid_count), 0) as retention_30d_muid_count
         from stat_kch_install_retention_count
         where bj_date >= '2022-03-28'
           and bj_date <= '2022-04-10'
           and campaign_id in (
             select
                 campaign_id
             from tmp_campaign_id
         )
         group by campaign_id,
                  bj_date,
                  country
     ),
     tmp_all_kch_install_info        as (
         select
             campaign_id,
             date,
             sum(install) as all_country_kch_installs
         from all_country_retention_info
         group by campaign_id,
                  date
     ),
     retention_info                  as (
         select
             campaign_id,
             date,
             nvl(sum(install), 0)                  as install,
             nvl(sum(muid_install), 0)             as muid_install,
             nvl(sum(retention_1d_count), 0)       as retention_1d_count,
             nvl(sum(retention_1d_muid_count), 0)  as retention_1d_muid_count,
             nvl(sum(retention_2d_count), 0)       as retention_2d_count,
             nvl(sum(retention_2d_muid_count), 0)  as retention_2d_muid_count,
             nvl(sum(retention_3d_count), 0)       as retention_3d_count,
             nvl(sum(retention_3d_muid_count), 0)  as retention_3d_muid_count,
             nvl(sum(retention_7d_count), 0)       as retention_7d_count,
             nvl(sum(retention_7d_muid_count), 0)  as retention_7d_muid_count,
             nvl(sum(retention_14d_count), 0)      as retention_14d_count,
             nvl(sum(retention_14d_muid_count), 0) as retention_14d_muid_count,
             nvl(sum(retention_30d_count), 0)      as retention_30d_count,
             nvl(sum(retention_30d_muid_count), 0) as retention_30d_muid_count
         from all_country_retention_info
         where 1 = 1
           and country = 'CA'
         group by campaign_id,
                  date
     ),
     tmp_joined_data                 as (
         select
             case when rs.date is not null then rs.date else info.date end as date,
             case
                 when rs.campaign_id is not null
                     then rs.campaign_id
                     else info.campaign_id end                             as campaign_id,
             spend,                                                                    -- 留spend是否为空方便后续判断是否有roi
             nvl(installs, 0)                                              as ua_installs,
             nvl(clicks, 0)                                                as ua_clicks,
             nvl(impressions, 0)                                           as ua_impressions,
             nvl(all_kch.all_country_kch_installs, 0)                      as all_country_kch_installs,
             nvl(all_dh.all_country_dh_installs, 0)                        as all_country_dh_installs,
             install                                                       as install, -- 留install和muid_install是否为空方便后续判断是否有retention
             muid_install                                                  as muid_install,
             nvl(retention_1d_count, 0)                                    as retention_1d_count,
             nvl(retention_1d_muid_count, 0)                               as retention_1d_muid_count,
             nvl(retention_2d_count, 0)                                    as retention_2d_count,
             nvl(retention_2d_muid_count, 0)                               as retention_2d_muid_count,
             nvl(retention_3d_count, 0)                                    as retention_3d_count,
             nvl(retention_3d_muid_count, 0)                               as retention_3d_muid_count,
             nvl(retention_7d_count, 0)                                    as retention_7d_count,
             nvl(retention_7d_muid_count, 0)                               as retention_7d_muid_count,
             nvl(retention_14d_count, 0)                                   as retention_14d_count,
             nvl(retention_14d_muid_count, 0)                              as retention_14d_muid_count,
             nvl(retention_30d_count, 0)                                   as retention_30d_count,
             nvl(retention_30d_muid_count, 0)                              as retention_30d_muid_count,
             nvl(day0_ads_rev, 0.0)                                        as day0_ads_rev,
             nvl(day0_iap_rev, 0.0)                                        as day0_iap_rev,
             nvl(day0_ads_rev_include_fb, 0)                               as day0_ads_rev_include_fb,
             nvl(day1_ads_rev, 0.0)                                        as day1_ads_rev,
             nvl(day1_iap_rev, 0.0)                                        as day1_iap_rev,
             nvl(day1_ads_rev_include_fb, 0)                               as day1_ads_rev_include_fb,
             nvl(day2_ads_rev, 0.0)                                        as day2_ads_rev,
             nvl(day2_iap_rev, 0.0)                                        as day2_iap_rev,
             nvl(day2_ads_rev_include_fb, 0)                               as day2_ads_rev_include_fb,
             nvl(day3_ads_rev, 0.0)                                        as day3_ads_rev,
             nvl(day3_iap_rev, 0.0)                                        as day3_iap_rev,
             nvl(day3_ads_rev_include_fb, 0)                               as day3_ads_rev_include_fb,
             nvl(day7_ads_rev, 0.0)                                        as day7_ads_rev,
             nvl(day7_iap_rev, 0.0)                                        as day7_iap_rev,
             nvl(day7_ads_rev_include_fb, 0)                               as day7_ads_rev_include_fb,
             nvl(day14_ads_rev, 0.0)                                       as day14_ads_rev,
             nvl(day14_iap_rev, 0.0)                                       as day14_iap_rev,
             nvl(day14_ads_rev_include_fb, 0)                              as day14_ads_rev_include_fb,
             nvl(day30_ads_rev, 0.0)                                       as day30_ads_rev,
             nvl(day30_iap_rev, 0.0)                                       as day30_iap_rev,
             nvl(day30_ads_rev_include_fb, 0)                              as day30_ads_rev_include_fb
         from campaign_rs                       as rs
             full join -- 不能舍弃掉没有spend的kch安装数据
                           retention_info       as info
                       on
                                   rs.date = info.date
                               and rs.campaign_id = info.campaign_id
             left join
                       tmp_all_kch_install_info as all_kch -- kch的数据在retention info中一定有
                       on
                                   info.date = all_kch.date
                               and info.campaign_id = all_kch.campaign_id
             left join
                       tmp_all_dh_install_info  as all_dh -- dh的数据在campaign rs中一定有，因为没有过滤过spend
                       on
                                   rs.date = all_dh.date
                               and rs.campaign_id = all_dh.campaign_id
     )
select
    date,
    tj.campaign_id,
    campaign_name,
    ua_media,
    app_name,
    campaign_living_days,
    country_str,
    spend,
    ua_installs,
    ua_clicks,
    ua_impressions,
    all_country_kch_installs,
    all_country_dh_installs,
    install,
    muid_install,
    nvl(retention_1d_count, 0)       as retention_1d_count,
    nvl(retention_1d_muid_count, 0)  as retention_1d_muid_count,
    nvl(retention_2d_count, 0)       as retention_2d_count,
    nvl(retention_2d_muid_count, 0)  as retention_2d_muid_count,
    nvl(retention_3d_count, 0)       as retention_3d_count,
    nvl(retention_3d_muid_count, 0)  as retention_3d_muid_count,
    nvl(retention_7d_count, 0)       as retention_7d_count,
    nvl(retention_7d_muid_count, 0)  as retention_7d_muid_count,
    nvl(retention_14d_count, 0)      as retention_14d_count,
    nvl(retention_14d_muid_count, 0) as retention_14d_muid_count,
    nvl(retention_30d_count, 0)      as retention_30d_count,
    nvl(retention_30d_muid_count, 0) as retention_30d_muid_count,
    nvl(day0_ads_rev, 0.0)           as day0_ads_rev,
    nvl(day0_iap_rev, 0.0)           as day0_iap_rev,
    nvl(day0_ads_rev_include_fb, 0)  as day0_ads_rev_include_fb,
    nvl(day1_ads_rev, 0.0)           as day1_ads_rev,
    nvl(day1_iap_rev, 0.0)           as day1_iap_rev,
    nvl(day1_ads_rev_include_fb, 0)  as day1_ads_rev_include_fb,
    nvl(day2_ads_rev, 0.0)           as day2_ads_rev,
    nvl(day2_iap_rev, 0.0)           as day2_iap_rev,
    nvl(day2_ads_rev_include_fb, 0)  as day2_ads_rev_include_fb,
    nvl(day3_ads_rev, 0.0)           as day3_ads_rev,
    nvl(day3_iap_rev, 0.0)           as day3_iap_rev,
    nvl(day3_ads_rev_include_fb, 0)  as day3_ads_rev_include_fb,
    nvl(day7_ads_rev, 0.0)           as day7_ads_rev,
    nvl(day7_iap_rev, 0.0)           as day7_iap_rev,
    nvl(day7_ads_rev_include_fb, 0)  as day7_ads_rev_include_fb,
    nvl(day14_ads_rev, 0.0)          as day14_ads_rev,
    nvl(day14_iap_rev, 0.0)          as day14_iap_rev,
    nvl(day14_ads_rev_include_fb, 0) as day14_ads_rev_include_fb,
    nvl(day30_ads_rev, 0.0)          as day30_ads_rev,
    nvl(day30_iap_rev, 0.0)          as day30_iap_rev,
    nvl(day30_ads_rev_include_fb, 0) as day30_ads_rev_include_fb
from tmp_joined_data   as tj
    inner join
tmp_campaign_attribute as attr
on
    tj.campaign_id = attr.campaign_id
;



with campaign_cost  as ( -- 有开销的Campaign数据，Campaign id一定非空
    select
        app_name,
        country,
        campaign_id,
        media_source as ua_media,
        date,
        sum(spend)   as spend
    from mid_dh_ua_data
    where date >= '2022-03-28'
      and date <= '2022-04-10'
      and app_name in ('aiolos_gp')
      and country in ('CA')
    group by date,
             app_name,
             country,
             campaign_id,
             media_source
),
     -- 基于campaign的rev数据，注意，mid_ilrd_campaign_roi_total_rev存在campaign id为空的情况
     campaign_rev   as (
         select
             app_name,
             country,
             campaign_id,
             bj_date                      as date,
             ua_media,
             nvl(sum(day0_ads_rev), 0.0)  as day0_ads_rev,
             nvl(sum(day0_iap_rev), 0.0)  as day0_iap_rev,
             nvl(sum(day1_ads_rev), 0.0)  as day1_ads_rev,
             nvl(sum(day1_iap_rev), 0.0)  as day1_iap_rev,
             nvl(sum(day2_ads_rev), 0.0)  as day2_ads_rev,
             nvl(sum(day2_iap_rev), 0.0)  as day2_iap_rev,
             nvl(sum(day3_ads_rev), 0.0)  as day3_ads_rev,
             nvl(sum(day3_iap_rev), 0.0)  as day3_iap_rev,
             nvl(sum(day7_ads_rev), 0.0)  as day7_ads_rev,
             nvl(sum(day7_iap_rev), 0.0)  as day7_iap_rev,
             nvl(sum(day14_ads_rev), 0.0) as day14_ads_rev,
             nvl(sum(day14_iap_rev), 0.0) as day14_iap_rev,
             nvl(sum(day30_ads_rev), 0.0) as day30_ads_rev,
             nvl(sum(day30_iap_rev), 0.0) as day30_iap_rev
         from mid_ilrd_campaign_roi_total_rev
         where bj_date >= '2022-03-28'
           and bj_date <= '2022-04-10'
           and app_name in ('aiolos_gp')
           and country in ('CA')
         group by bj_date,
                  app_name,
                  country,
                  campaign_id,
                  ua_media
     ),
     campaign_rs    as (
         select
             cost.date,
             cost.app_name,
             cost.country,
             cost.ua_media,
             sum(spend)                   as spend,
             nvl(sum(day0_ads_rev), 0.0)  as day0_ads_rev,
             nvl(sum(day0_iap_rev), 0.0)  as day0_iap_rev,
             nvl(sum(day1_ads_rev), 0.0)  as day1_ads_rev,
             nvl(sum(day1_iap_rev), 0.0)  as day1_iap_rev,
             nvl(sum(day2_ads_rev), 0.0)  as day2_ads_rev,
             nvl(sum(day2_iap_rev), 0.0)  as day2_iap_rev,
             nvl(sum(day3_ads_rev), 0.0)  as day3_ads_rev,
             nvl(sum(day3_iap_rev), 0.0)  as day3_iap_rev,
             nvl(sum(day7_ads_rev), 0.0)  as day7_ads_rev,
             nvl(sum(day7_iap_rev), 0.0)  as day7_iap_rev,
             nvl(sum(day14_ads_rev), 0.0) as day14_ads_rev,
             nvl(sum(day14_iap_rev), 0.0) as day14_iap_rev,
             nvl(sum(day30_ads_rev), 0.0) as day30_ads_rev,
             nvl(sum(day30_iap_rev), 0.0) as day30_iap_rev
         from campaign_cost         as cost
             left join campaign_rev as rev
                       on cost.date = rev.date
                           and cost.campaign_id = rev.campaign_id
                           and cost.ua_media = rev.ua_media
                           and cost.app_name = rev.app_name
                           and cost.country = rev.country
         where cost.spend > 0
         group by cost.date,
                  cost.ua_media,
                  cost.app_name,
                  cost.country
     ),
     no_campaign_rs as (
         select
             bj_date                      as date,
             ua_media,
             app_name,
             country,
             0.0                          as spend,
             nvl(sum(day0_ads_rev), 0.0)  as day0_ads_rev,
             nvl(sum(day0_iap_rev), 0.0)  as day0_iap_rev,
             nvl(sum(day1_ads_rev), 0.0)  as day1_ads_rev,
             nvl(sum(day1_iap_rev), 0.0)  as day1_iap_rev,
             nvl(sum(day2_ads_rev), 0.0)  as day2_ads_rev,
             nvl(sum(day2_iap_rev), 0.0)  as day2_iap_rev,
             nvl(sum(day3_ads_rev), 0.0)  as day3_ads_rev,
             nvl(sum(day3_iap_rev), 0.0)  as day3_iap_rev,
             nvl(sum(day7_ads_rev), 0.0)  as day7_ads_rev,
             nvl(sum(day7_iap_rev), 0.0)  as day7_iap_rev,
             nvl(sum(day14_ads_rev), 0.0) as day14_ads_rev,
             nvl(sum(day14_iap_rev), 0.0) as day14_iap_rev,
             nvl(sum(day30_ads_rev), 0.0) as day30_ads_rev,
             nvl(sum(day30_iap_rev), 0.0) as day30_iap_rev
         from mid_ilrd_campaign_roi_total_rev
         where bj_date >= '2022-03-28'
           and bj_date <= '2022-04-10'
           and app_name in ('aiolos_gp')
           and country in ('CA')
           and ua_media in ('Default restricted')
           and bj_date in (
             select distinct date from campaign_rs group by date having sum(spend) > 0
         )
         group by bj_date,
                  ua_media,
                  app_name,
                  country
     ),
     rs             as (
         select
             date,
             app_name,
             country,
             ua_media,
             spend,
             nvl(day0_ads_rev, 0.0)  as day0_ads_rev,
             nvl(day0_iap_rev, 0.0)  as day0_iap_rev,
             nvl(day1_ads_rev, 0.0)  as day1_ads_rev,
             nvl(day1_iap_rev, 0.0)  as day1_iap_rev,
             nvl(day2_ads_rev, 0.0)  as day2_ads_rev,
             nvl(day2_iap_rev, 0.0)  as day2_iap_rev,
             nvl(day3_ads_rev, 0.0)  as day3_ads_rev,
             nvl(day3_iap_rev, 0.0)  as day3_iap_rev,
             nvl(day7_ads_rev, 0.0)  as day7_ads_rev,
             nvl(day7_iap_rev, 0.0)  as day7_iap_rev,
             nvl(day14_ads_rev, 0.0) as day14_ads_rev,
             nvl(day14_iap_rev, 0.0) as day14_iap_rev,
             nvl(day30_ads_rev, 0.0) as day30_ads_rev,
             nvl(day30_iap_rev, 0.0) as day30_iap_rev
         from campaign_rs
         union
         select
             date,
             app_name,
             country,
             case when ua_media = 'Default restricted' then 'Facebook' else ua_media end as ua_media,
             spend,
             nvl(day0_ads_rev, 0.0)                                                      as day0_ads_rev,
             nvl(day0_iap_rev, 0.0)                                                      as day0_iap_rev,
             nvl(day1_ads_rev, 0.0)                                                      as day1_ads_rev,
             nvl(day1_iap_rev, 0.0)                                                      as day1_iap_rev,
             nvl(day2_ads_rev, 0.0)                                                      as day2_ads_rev,
             nvl(day2_iap_rev, 0.0)                                                      as day2_iap_rev,
             nvl(day3_ads_rev, 0.0)                                                      as day3_ads_rev,
             nvl(day3_iap_rev, 0.0)                                                      as day3_iap_rev,
             nvl(day7_ads_rev, 0.0)                                                      as day7_ads_rev,
             nvl(day7_iap_rev, 0.0)                                                      as day7_iap_rev,
             nvl(day14_ads_rev, 0.0)                                                     as day14_ads_rev,
             nvl(day14_iap_rev, 0.0)                                                     as day14_iap_rev,
             nvl(day30_ads_rev, 0.0)                                                     as day30_ads_rev,
             nvl(day30_iap_rev, 0.0)                                                     as day30_iap_rev
         from no_campaign_rs
     ),
     all_media_rs   as ( -- 要去掉Facebook没有开销，但是有Default restricted的情况
         select
             date,
             app_name,
             country,
             ua_media,
             sum(spend)                   as _spend,
             nvl(sum(day0_ads_rev), 0.0)  as day0_ads_rev,
             nvl(sum(day0_iap_rev), 0.0)  as day0_iap_rev,
             nvl(sum(day1_ads_rev), 0.0)  as day1_ads_rev,
             nvl(sum(day1_iap_rev), 0.0)  as day1_iap_rev,
             nvl(sum(day2_ads_rev), 0.0)  as day2_ads_rev,
             nvl(sum(day2_iap_rev), 0.0)  as day2_iap_rev,
             nvl(sum(day3_ads_rev), 0.0)  as day3_ads_rev,
             nvl(sum(day3_iap_rev), 0.0)  as day3_iap_rev,
             nvl(sum(day7_ads_rev), 0.0)  as day7_ads_rev,
             nvl(sum(day7_iap_rev), 0.0)  as day7_iap_rev,
             nvl(sum(day14_ads_rev), 0.0) as day14_ads_rev,
             nvl(sum(day14_iap_rev), 0.0) as day14_iap_rev,
             nvl(sum(day30_ads_rev), 0.0) as day30_ads_rev,
             nvl(sum(day30_iap_rev), 0.0) as day30_iap_rev
         from rs
         group by date,
                  app_name,
                  country,
                  ua_media
         having (ua_media != 'Organic' and _spend > 0) or ua_media = 'Organic' -- 注意别过滤掉了Organic
     )
select
    date,
    app_name,
    country,
    sum(_spend)                  as spend,
    nvl(sum(day0_ads_rev), 0.0)  as day0_ads_rev,
    nvl(sum(day0_iap_rev), 0.0)  as day0_iap_rev,
    nvl(sum(day1_ads_rev), 0.0)  as day1_ads_rev,
    nvl(sum(day1_iap_rev), 0.0)  as day1_iap_rev,
    nvl(sum(day2_ads_rev), 0.0)  as day2_ads_rev,
    nvl(sum(day2_iap_rev), 0.0)  as day2_iap_rev,
    nvl(sum(day3_ads_rev), 0.0)  as day3_ads_rev,
    nvl(sum(day3_iap_rev), 0.0)  as day3_iap_rev,
    nvl(sum(day7_ads_rev), 0.0)  as day7_ads_rev,
    nvl(sum(day7_iap_rev), 0.0)  as day7_iap_rev,
    nvl(sum(day14_ads_rev), 0.0) as day14_ads_rev,
    nvl(sum(day14_iap_rev), 0.0) as day14_iap_rev,
    nvl(sum(day30_ads_rev), 0.0) as day30_ads_rev,
    nvl(sum(day30_iap_rev), 0.0) as day30_iap_rev
from all_media_rs
group by date,
         app_name,
         country
having spend > 0
