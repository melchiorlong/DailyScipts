-- 备份
-- create table temp_dws_ua_muid_campaign_detail_backup_20220415 as
-- select *
-- from dws_ua_muid_campaign_detail;
--
--
-- create table temp_mid_ilrd_campaign_roi_total_rev_backup_20220415 as
-- select *
-- from mid_ilrd_campaign_roi_total_rev;
--
--
-- create table temp_dws_ua_rev_dau_campaign_d_backup_20220415 as
-- select *
-- from dws_ua_rev_dau_campaign_d;
--
-- create table temp_dws_ua_spend_dnu_country_media_d_backup_20220415 as
-- select *
-- from dws_ua_spend_dnu_country_media_d;

drop table if exists iap_temp_log_history;
create table iap_temp_log_history as
with temp as (
    select
        muid,
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
                 else 'null' end)                                  as app_name,
        trunc(dateadd(
                hour, 8,
                case
                    when abs(datediff(day, action_time, service_log_time)) > 2
                        then service_log_time
                        else action_time end
            ))                                                     as rev_bj_date,
        product_price * 0.7                                        as iap_rev,
        trunc(convert_timezone('Asia/Shanghai', service_log_time)) as log_bj_date
    from iap_log log
    where (
            (
                        app_package_name = 'art.color.planet.oil.paint.canvas.number'
                    and app_version_code >= 30
                )
            or
            (
                        app_package_name = 'art.color.planet.oil.paint.canvas.number.free'
                    and app_version_code >= 35
                )
            or
            (
                        app_package_name = 'art.color.planet.paint.by.number.game.puzzle'
                    and app_version_code >= 16
                    and app_version_code >= 18
                )
            or
            (
                        app_package_name = 'art.color.planet.jigsaw.puzzle.online.free'
                    and app_version_code >= 8
                )
            or
            (
                        app_package_name = 'art.color.planet.jigsaw.puzzle.online'
                    and app_version_code >= 16
                )
            or
            (
                        app_package_name = 'happy.puzzle.merge.block.shoot2048.number.game.free'
                    and app_version_code >= 4
                )
            or
            (
                        app_package_name = 'happy.puzzle.merge.block.shoot2048.number.game'
                    and app_version_code >= 2
                )
        )
      and action_type = 3
      and event = 'pay_success'
      and trunc(convert_timezone('Asia/Shanghai', service_log_time)) >= '2022-02-11'
      and trunc(convert_timezone('Asia/Shanghai', service_log_time)) <= '2022-04-15'
)
select
    muid,
    rev_bj_date,
    sum(iap_rev) as iap_rev,
    log_bj_date
from temp
group by muid,
         rev_bj_date,
         log_bj_date;


-- merge iap_rev into dws
update dws_ua_muid_campaign_detail
set iap_rev = iap_temp_log_history.iap_rev
from iap_temp_log_history
where dws_ua_muid_campaign_detail.muid = iap_temp_log_history.muid
  and dws_ua_muid_campaign_detail.rev_bj_date = iap_temp_log_history.rev_bj_date
  and dws_ua_muid_campaign_detail.log_bj_date = iap_temp_log_history.log_bj_date;

delete
from iap_temp_log_history
    using dws_ua_muid_campaign_detail
where iap_temp_log_history.muid = dws_ua_muid_campaign_detail.muid
  and iap_temp_log_history.rev_bj_date = dws_ua_muid_campaign_detail.rev_bj_date
  and iap_temp_log_history.log_bj_date = dws_ua_muid_campaign_detail.log_bj_date;

insert into dws_ua_muid_campaign_detail (muid, rev_bj_date, iap_rev, log_bj_date)
select
    muid,
    rev_bj_date,
    iap_rev,
    log_bj_date
from iap_temp_log_history;



update dws_ua_muid_campaign_detail
set app_name        = muid_dimension.app_name,
    ua_media        = muid_dimension.media_source,
    country         = muid_dimension.kch_country,
    campaign_id     = muid_dimension.campaign_id,
    install_bj_date = trunc(muid_dimension.install_bj_datetime)
from muid_dimension
where dws_ua_muid_campaign_detail.muid = muid_dimension.muid
  and dws_ua_muid_campaign_detail.install_bj_date is null;

-- update day_dimension
update dws_ua_muid_campaign_detail
set day_dimension = datediff(day, install_bj_date, rev_bj_date)
where day_dimension is null
  and install_bj_date is not null
  and rev_bj_date is not null;



with temp as (
    select
        muid,
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
                 else 'null' end)                                  as app_name,
        trunc(dateadd(
                hour, 8,
                case
                    when abs(datediff(day, action_time, service_log_time)) > 2
                        then service_log_time
                        else action_time end
            ))                                                     as rev_bj_date,
        product_price * 0.7                                        as iap_rev,
        trunc(convert_timezone('Asia/Shanghai', service_log_time)) as log_bj_date
    from iap_log log
    where (
            (
                        app_package_name = 'art.color.planet.oil.paint.canvas.number'
                    and app_version_code >= 30
                )
            or
            (
                        app_package_name = 'art.color.planet.oil.paint.canvas.number.free'
                    and app_version_code >= 35
                )
            or
            (
                        app_package_name = 'art.color.planet.paint.by.number.game.puzzle'
                    and app_version_code >= 16
                    and app_version_code >= 18
                )
            or
            (
                        app_package_name = 'art.color.planet.jigsaw.puzzle.online.free'
                    and app_version_code >= 8
                )
            or
            (
                        app_package_name = 'art.color.planet.jigsaw.puzzle.online'
                    and app_version_code >= 16
                )
            or
            (
                        app_package_name = 'happy.puzzle.merge.block.shoot2048.number.game.free'
                    and app_version_code >= 4
                )
            or
            (
                        app_package_name = 'happy.puzzle.merge.block.shoot2048.number.game'
                    and app_version_code >= 2
                )
        )
      and action_type = 3
      and event = 'pay_success'
      and trunc(convert_timezone('Asia/Shanghai', service_log_time)) >= '2022-02-11'
      and trunc(convert_timezone('Asia/Shanghai', service_log_time)) <= '2022-04-15'
)
select
    muid,
    rev_bj_date,
    sum(iap_rev) as iap_rev,
    log_bj_date
from temp
where 1 = 1
  and muid in ('5fd61aaa-7a34-4b43-81f6-8c003851269b', '2aa64c62-ce43-4d01-af05-f5e0360f2331',
               '7719e7d8-8448-407d-9dcc-82412d7af3da', 'b014afb1-05f5-4a72-a25b-4ed0011d4c11',
               'c1555956-e624-4542-a4c5-d9a3e174d071', '600e5955-347c-4eb8-95d4-4775bb4a5f99',
               'bacc2441-7bfd-4b1e-957c-8203ff1257ed', 'e48b3467-d85b-4d1a-a380-de927c25eab4',
               'e2f917e8-2bb7-4c11-9586-5413fac70c68')
group by muid,
         rev_bj_date,
         log_bj_date;













