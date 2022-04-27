create external table spectrum.dwd_poseidon_advertisement_info_detail
    (
    action_bj_date date,
    app_package_name varchar(64),
    muid varchar(64),
    placement_name varchar(64),
    vendor varchar(64),
    app_version_code int,
    should_display_cnt int,
    click_cnt int,
    impr_cnt int,
    unban_cnt int,
    ban_cnt int,
    session_start_cnt int
    )
    partitioned by (log_bj_date date)
    row format serde 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
    with serdeproperties ('serialization.format'='1')
    stored as
    inputformat 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat'
    outputformat 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
    location 's3://gvprod/data_warehouse/dwd/dwd_poseidon_advertisement_info_detail/'
;

-- insert into dws_muid_advertisement_info (action_bj_date,
--                                          app_name,
--                                          placement_name,
--                                          vendor,
--                                          app_version_code,
--                                          kch_country,
--                                          app_install_version,
--                                          install_bj_datetime,
--                                          media_source,
--                                          sum_should_display_cnt,
--                                          sum_click_cnt,
--                                          sum_impr_cnt,
--                                          sum_ban_cnt,
--                                          sum_unban_cnt,
--                                          sum_session_start_cnt,
--                                          log_bj_date)
select
    dpaid.action_bj_date,
    (case dpaid.app_package_name
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
             else 'null' end)     as app_name,
    dpaid.placement_name,
    dpaid.vendor,
    dpaid.app_version_code,
    case
        when md.kch_country is not null
            then md.kch_country
            else 'Unknown' end    as kch_country,
    md.app_install_version,
    md.install_bj_datetime,
    md.media_source               as ua_media,
    sum(dpaid.should_display_cnt) as sum_should_display_cnt,
    sum(dpaid.click_cnt)          as sum_click_cnt,
    sum(dpaid.impr_cnt)           as sum_impr_cnt,
    sum(dpaid.ban_cnt)            as sum_ban_cnt,
    sum(dpaid.unban_cnt)          as sum_unban_cnt,
    sum(dpaid.session_start_cnt)  as sum_session_start_cnt,
    dpaid.log_bj_date
from spectrum.dwd_poseidon_advertisement_info_detail dpaid
    left join muid_dimension                         md
              on md.muid = dpaid.muid
where dpaid.log_bj_date = '2022-03-01' -- todo KchCountry 有可能延迟上报，是否需要同步近 7 or 14 天数据。等以后再说。
group by dpaid.action_bj_date,
         dpaid.app_package_name,
         dpaid.placement_name,
         dpaid.vendor,
         dpaid.app_version_code,
         kch_country,
         md.app_install_version,
         md.install_bj_datetime,
         md.media_source,
         dpaid.log_bj_date
;



create table temp_mid_ilrd_should_display_backup_20220411 as
select *
from mid_ilrd_should_display;

select
    trunc(bj_date),
    sum(should_display),
    sum(impr),
    count(1)
from temp_mid_ilrd_should_display_backup_20220411
where app_name = 'aiolos_gp'
  and placement = 'hebi'
group by trunc(bj_date)
;

select
    trunc(bj_date),
    sum(should_display),
    sum(impr),
    count(1)
from mid_ilrd_should_display
where app_name = 'aiolos_gp'
  and placement = 'hebi'
group by trunc(bj_date)
;



select
    trunc(date),
    sum(dau_flurry)
from mid_dh_flurry_daily_usage
where app_name = 'aiolos_gp'
  and trunc(date) >= '2022-03-01'
group by trunc(date)
;

select
    trunc(date),
    sum(impr)
from mid_dh_market_data
where app_name = 'aiolos_gp'
  and trunc(date) >= '2022-03-01'
group by trunc(date);


create table temp_dwd_poseidon_advertisement_info_detail_20220408 as
select
    trunc(dateadd(
            hour, 8,
            case
                when abs(datediff(day, action_time, service_log_time)) > 2
                    then service_log_time
                    else action_time end
        ))                                                           as action_bj_date,
    app_package_name,
    muid,
    placement_name,
    vendor,
    app_version_code,
    sum(case action_type when 'ad_should_display' then 1 else 0 end) as should_display_cnt,
    sum(case action_type when 'click' then 1 else 0 end)             as click_cnt,
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
                else 0 end)::int                                     as impr_cnt,
    sum(case action_type when 'leppa' then 1 else 0 end)             as unban_cnt,
    sum(case action_type when 'apple' then 1 else 0 end)             as ban_cnt,
    sum(case action_type when 'session_start' then 1 else 0 end)     as session_start_cnt,
    trunc(dateadd(hour, 8, log_time))                                as log_bj_date
from spectrum.fact_ivt_poseidon_log
where 1 = 1
  and action_type in ('ad_should_display', 'impression', 'apple', 'leppa', 'session_start', 'click')
  and trunc(dateadd(hour, 8, log_time)) = '2022-03-29'
group by action_bj_date,
         app_package_name,
         muid,
         placement_name,
         vendor,
         app_version_code,
         log_bj_date
;



drop table dws_muid_advertisement_info;
create table dws_muid_advertisement_info
(
    action_bj_date         date,
    app_name               varchar(64),
    placement_name         varchar(64),
    vendor                 varchar(64),
    app_version_code       int,
    kch_country            varchar(64),
    app_install_version    int,
    install_bj_datetime    date,
    media_source           varchar(64),
    sum_should_display_cnt int,
    sum_click_cnt          int,
    sum_impr_cnt           int,
    sum_ban_cnt            int,
    sum_unban_cnt          int,
    sum_session_start_cnt  int,
    log_bj_date            date
);

insert into dws_muid_advertisement_info (action_bj_date,
                                         app_name,
                                         placement_name,
                                         vendor,
                                         app_version_code,
                                         kch_country,
                                         app_install_version,
                                         install_bj_datetime,
                                         media_source,
                                         sum_should_display_cnt,
                                         sum_click_cnt,
                                         sum_impr_cnt,
                                         sum_ban_cnt,
                                         sum_unban_cnt,
                                         sum_session_start_cnt,
                                         log_bj_date)
select
    dpaid.action_bj_date,
    (case dpaid.app_package_name
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
             else 'null' end)     as app_name,
    dpaid.placement_name,
    dpaid.vendor,
    dpaid.app_version_code,
    case
        when md.kch_country is not null
            then md.kch_country
            else 'Unknown' end    as kch_country,
    md.app_install_version,
    md.install_bj_datetime,
    md.media_source               as ua_media,
    sum(dpaid.should_display_cnt) as sum_should_display_cnt,
    sum(dpaid.click_cnt)          as sum_click_cnt,
    sum(dpaid.impr_cnt)           as sum_impr_cnt,
    sum(dpaid.ban_cnt)            as sum_ban_cnt,
    sum(dpaid.unban_cnt)          as sum_unban_cnt,
    sum(dpaid.session_start_cnt)  as sum_session_start_cnt,
    dpaid.log_bj_date
from temp_dwd_poseidon_advertisement_info_detail_20220408 dpaid
    left join muid_dimension                              md
              on md.muid = dpaid.muid
where dpaid.log_bj_date = '2022-03-29'
group by dpaid.action_bj_date,
         dpaid.app_package_name,
         dpaid.placement_name,
         dpaid.vendor,
         dpaid.app_version_code,
         kch_country,
         md.app_install_version,
         md.install_bj_datetime,
         md.media_source,
         dpaid.log_bj_date
;


drop table ads_monetization_psd_ad_info;
create table ads_monetization_psd_ad_info
(
    action_bj_date date,
    app_name       varchar(64),
    placement_name varchar(64),
    vendor         varchar(64),
    kch_country    varchar(64),
    impression     int,
    click          int,
    should_display int,
    log_bj_date    date
);



insert into ads_monetization_psd_ad_info (action_bj_date,
                                          app_name,
                                          placement_name,
                                          vendor,
                                          kch_country,
                                          impression,
                                          click,
                                          should_display,
                                          log_bj_date)
select
    action_bj_date,
    app_name,
    placement_name,
    vendor,
    kch_country,
    sum(sum_impr_cnt)           as sum_impr,
    sum(sum_click_cnt)          as sum_click,
    sum(sum_should_display_cnt) as sum_sd,
    log_bj_date
from dws_muid_advertisement_info
where 1 = 1
  and log_bj_date = '{exe_date}'
  and (
        (app_name = 'saori_gp' and app_version_code >= 31) or (app_name = 'saori_ip' and app_version_code >= 21) or
        (app_name = 'saga_gp' and app_version_code >= 4) or (app_name = 'aiolos_ip' and app_version_code >= 17) or
        (app_name = 'dohko_ip' and app_version_code >= 37) or (app_name = 'dohko_gp' and app_version_code >= 43) or
        (app_name = 'aiolos_gp' and app_version_code >= 12) or (app_name = 'saga_ip' and app_version_code >= 2)
    )
group by action_bj_date,
         app_name,
         placement_name,
         vendor,
         kch_country,
         log_bj_date
;


create table temp_mid_ilrd_should_display_20220408 as
select *
from mid_ilrd_should_display;


delete
from temp_mid_ilrd_should_display_20220408
where bj_date >= '2022-03-29';



insert into temp_mid_ilrd_should_display_20220408(bj_date, app_name, country, placement, should_display, impr)
with log_temp as (
    select
        trunc(dateadd(
                hour, 8,
                case
                    when abs(datediff(day, action_time, service_log_time)) > 2
                        then service_log_time
                        else action_time end
            ))                                                           as bj_date,
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
            '2022-03-29',
            dateadd(hour, 8, log_time)
        ) between -1 and 24
      and bj_date = '2022-03-29'
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
             bj_date,
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




select trunc(action_bj_date),count(1)
from ads_monetization_psd_ad_info
group by trunc(action_bj_date);

select trunc(log_bj_date),count(1)
from ads_monetization_psd_ad_info
group by trunc(log_bj_date);


select trunc(log_bj_date),count(1)
from ads_monetization_psd_ad_info
group by trunc(log_bj_date);

