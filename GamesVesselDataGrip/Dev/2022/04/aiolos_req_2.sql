-- 分别查一下
-- begin=0
-- US
-- 用户其他行为数据
-- 条件：
-- Install Date：2021-12-01 ~ 2022-01-31
-- Session Date：2021-12-01 ~ 2022-03-31
--
-- 产品：Aiolos_gp / Aiolos_ip(Phone) / Aiolos_ip(Pad)
-- 内容：
-- 1. 2/3用户中Posedion上有行为的用户，各个行为的数量 Session start / 3种广告(show) / 封禁 / IAP
-- 2. Posedion上有session start的用户，session分布在 1天 2天 3天 3天以上的用户数
-- 3. Posedion上有session start的用户，session分布在 1次 2次 3次 4次 4次以上的用户数
-- 4. 1/3有行为的用户，最后一个行为的分布及用户数


-- 1. 2/3用户中Posedion上有行为的用户，各个行为的数量 Session start / 3种广告(show) / 封禁 / IAP
with psd_act_muid as (
    select
        muid,
        sum(case when placement_name = 'hebi' then impr_cnt else 0 end)  as hebi_impr_cnt_sum,
        sum(case when placement_name = 'tora' then impr_cnt else 0 end)  as tora_impr_cnt_sum,
        sum(case when placement_name = 'tatsu' then impr_cnt else 0 end) as tatsu_impr_cnt_sum,
        sum(ban_cnt)                                                     as ban_cnt_sum,
        sum(click_cnt)                                                   as click_cnt_sum,
        sum(session_start_cnt)                                           as session_start_cnt_sum,
        sum(unban_cnt)                                                   as unban_cnt_sum,
        sum(should_display_cnt)                                          as should_display_cnt_sum,
        (hebi_impr_cnt_sum + tora_impr_cnt_sum + tatsu_impr_cnt_sum + ban_cnt_sum + click_cnt_sum +
         session_start_cnt_sum + unban_cnt_sum +
         should_display_cnt_sum)                                         as active_cnt
    from spectrum.dwd_poseidon_advertisement_info_detail
    where 1 = 1
      and app_package_name in ('art.color.planet.jigsaw.puzzle.online.free', 'art.color.planet.jigsaw.puzzle.online')
      and trunc(action_bj_date) >= '2021-12-01'
      and trunc(action_bj_date) <= '2022-03-31'
      and trunc(log_bj_date) >= '2021-11-20'
      and trunc(log_bj_date) <= '2022-04-10'
    group by muid
),
     pz_log       as (
         select distinct
             muid
         from puzzle_log
         where 1 = 1
           and trunc(convert_timezone('Asia/Shanghai', action_time)) <= '2022-03-31'
         group by muid
     ),
     ins_users    as (
         select distinct
             kch.app_name,
             case when kch.app_name = 'aiolos_gp' then 'android' else device_model end as device_model,
             md.muid,
             trunc(kch.bj_date_occurred)                                               as ins_date
         from dwd_ua_kch_install_info  kch
             inner join muid_dimension md on kch.kochava_device_id = md.kch_id
         where ins_date >= '2021-12-01'
           and ins_date <= '2022-01-31'
           and kch.country_code = 'US'
           and (kch.app_name = 'aiolos_gp' or (kch.app_name = 'aiolos_ip' and kch.device_model in ('iPhone', 'iPad')))
     ),
     iap_temp     as (
         select
             muid,
             count(1) as iap_cnt
         from iap_log
         where action_type = 3
           and app_package_name in
               ('art.color.planet.jigsaw.puzzle.online.free', 'art.color.planet.jigsaw.puzzle.online')
           and action_time >= '2021-12-01'
           and action_time <= '2022-03-31'
         group by muid
     )
select
    iu.app_name,
    iu.device_model,
    sum(case when pam.hebi_impr_cnt_sum > 0 then 1 else 0 end)                    as psd_hebi_impr_cnt_sum,
    sum(case when pam.tora_impr_cnt_sum > 0 then 1 else 0 end)                    as psd_tora_impr_cnt_sum,
    sum(case when pam.tatsu_impr_cnt_sum > 0 then 1 else 0 end)                   as psd_tatsu_impr_cnt_sum,
    sum(case when pam.ban_cnt_sum > 0 then 1 else 0 end)                          as psd_ban_cnt_sum,
    sum(case when pam.click_cnt_sum > 0 then 1 else 0 end)                        as psd_click_cnt_sum,
    sum(case when pam.session_start_cnt_sum > 0 then 1 else 0 end)                as psd_session_start_cnt_sum,
    sum(case when pam.unban_cnt_sum > 0 then 1 else 0 end)                        as psd_unban_cnt_sum,
    sum(case when pam.should_display_cnt_sum > 0 then 1 else 0 end)               as psd_should_display_cnt_sum,
    sum(case when pam.active_cnt > 0 then 1 else 0 end)                           as psd_active_cnt,
    sum(case when nvl(it.iap_cnt, 0) > 0 then 1 else 0 end) as iap_cnt
from psd_act_muid        pam
    inner join ins_users iu
               on iu.muid = pam.muid
    left join  pz_log    pl
               on pl.muid = pam.muid
    left join  iap_temp  it
               on it.muid = iu.muid
where pl.muid is null
group by iu.app_name,
         iu.device_model
;

-- 2. Posedion上有session start的用户，session分布在 1天 2天 3天 3天以上的用户数


with psd_act_muid as (
    select
        muid,
        count(distinct trunc(action_bj_date)) as session_start_cnt_sum
    from spectrum.dwd_poseidon_advertisement_info_detail
    where 1 = 1
      and app_package_name in
          ('art.color.planet.jigsaw.puzzle.online.free', 'art.color.planet.jigsaw.puzzle.online')
      and trunc(action_bj_date) >= '2021-12-01'
      and trunc(action_bj_date) <= '2022-03-31'
      and trunc(log_bj_date) >= '2021-11-20'
      and trunc(log_bj_date) <= '2022-04-10'
      and session_start_cnt > 0
    group by muid
),
     pz_log       as (
         select distinct
             muid
         from puzzle_log
         where 1 = 1
           and trunc(convert_timezone('Asia/Shanghai', action_time)) <= '2022-03-31'
         group by muid
     ),
     ins_users    as (
         select distinct
             kch.app_name,
             case when kch.app_name = 'aiolos_gp' then 'android' else device_model end as device_model,
             md.muid,
             trunc(kch.bj_date_occurred)                                               as ins_date
         from dwd_ua_kch_install_info  kch
             inner join muid_dimension md on kch.kochava_device_id = md.kch_id
         where ins_date >= '2021-12-01'
           and ins_date <= '2022-01-31'
           and kch.country_code = 'US'
           and (kch.app_name = 'aiolos_gp' or (kch.app_name = 'aiolos_ip' and kch.device_model in ('iPhone', 'iPad')))
     )
select
    iu.app_name,
    iu.device_model,
    sum(case when pam.session_start_cnt_sum = 1 then 1 else 0 end) as psd_session_start_1_cnt_sum,
    sum(case when pam.session_start_cnt_sum = 2 then 1 else 0 end) as psd_session_start_2_cnt_sum,
    sum(case when pam.session_start_cnt_sum = 3 then 1 else 0 end) as psd_session_start_3_cnt_sum,
    sum(case when pam.session_start_cnt_sum > 3 then 1 else 0 end) as psd_session_start_g3_cnt_sum
from psd_act_muid        pam
    inner join ins_users iu
               on iu.muid = pam.muid
    left join  pz_log    pl
               on pl.muid = pam.muid
where pl.muid is null
group by iu.app_name,
         iu.device_model
;


-- 3. Posedion上有session start的用户，session分布在 1次 2次 3次 4次 4次以上的用户数

with psd_act_muid as (
    select
        muid,
        sum(session_start_cnt) as session_start_cnt_sum
    from spectrum.dwd_poseidon_advertisement_info_detail
    where 1 = 1
      and app_package_name in ('art.color.planet.jigsaw.puzzle.online.free', 'art.color.planet.jigsaw.puzzle.online')
      and trunc(action_bj_date) >= '2021-12-01'
      and trunc(action_bj_date) <= '2022-03-31'
      and trunc(log_bj_date) >= '2021-11-20'
      and trunc(log_bj_date) <= '2022-04-10'
    group by muid
),
     pz_log       as (
         select distinct
             muid
         from puzzle_log
         where 1 = 1
           and trunc(convert_timezone('Asia/Shanghai', action_time)) <= '2022-03-31'
         group by muid
     ),
     ins_users    as (
         select distinct
             kch.app_name,
             case when kch.app_name = 'aiolos_gp' then 'android' else device_model end as device_model,
             md.muid,
             trunc(kch.bj_date_occurred)                                               as ins_date
         from dwd_ua_kch_install_info  kch
             inner join muid_dimension md on kch.kochava_device_id = md.kch_id
         where ins_date >= '2021-12-01'
           and ins_date <= '2022-01-31'
           and kch.country_code = 'US'
           and (kch.app_name = 'aiolos_gp' or (kch.app_name = 'aiolos_ip' and kch.device_model in ('iPhone', 'iPad')))
     )
select
    iu.app_name,
    iu.device_model,
    sum(case when pam.session_start_cnt_sum = 1 then 1 else 0 end) as psd_session_start_1_cnt_sum,
    sum(case when pam.session_start_cnt_sum = 2 then 1 else 0 end) as psd_session_start_2_cnt_sum,
    sum(case when pam.session_start_cnt_sum = 3 then 1 else 0 end) as psd_session_start_3_cnt_sum,
    sum(case when pam.session_start_cnt_sum = 4 then 1 else 0 end) as psd_session_start_4_cnt_sum,
    sum(case when pam.session_start_cnt_sum > 4 then 1 else 0 end) as psd_session_start_g4_cnt_sum
from psd_act_muid        pam
    inner join ins_users iu
               on iu.muid = pam.muid
    left join  pz_log    pl
               on pl.muid = pam.muid
where pl.muid is null
group by iu.app_name,
         iu.device_model
;


-- 4. 1/3有行为的用户， 能够关联到
-- 最后一个行为的分布及用户数
with pz_log        as (
    select
        muid
    from puzzle_log
    where 1 = 1
      and trunc(convert_timezone('Asia/Shanghai', action_time)) <= '2022-03-31'
    group by muid
    having count(case when action_type = 1 then 1 end) = 0
),
     last_act_temp as (
         select
             t1.muid,
             t1.action_type
         from (
             select
                 muid,
                 action_type,
                 rank()
                 over (partition by muid order by convert_timezone('Asia/Shanghai', action_time) desc) as rn
             from puzzle_log
             where 1 = 1
               and trunc(convert_timezone('Asia/Shanghai', action_time)) <= '2022-03-31'
               and muid in (select muid from pz_log)
         ) t1
         where t1.rn = 1
     ),
     ins_users     as (
         select distinct
             kch.app_name,
             case when kch.app_name = 'aiolos_gp' then 'android' else device_model end as device_model,
             md.muid,
             trunc(kch.bj_date_occurred)                                               as ins_date
         from dwd_ua_kch_install_info  kch
             inner join muid_dimension md on kch.kochava_device_id = md.kch_id
         where ins_date >= '2021-12-01'
           and ins_date <= '2022-01-31'
           and kch.country_code = 'US'
           and (kch.app_name = 'aiolos_gp' or (kch.app_name = 'aiolos_ip' and kch.device_model in ('iPhone', 'iPad')))
     )
select
    iu.app_name,
    iu.device_model,
    lat.action_type,
    count(distinct iu.muid)
from ins_users               iu
    inner join pz_log        pl
               on iu.muid = pl.muid
    inner join last_act_temp lat
               on lat.muid = iu.muid
group by iu.app_name,
         iu.device_model,
         lat.action_type
;


cancel 1077724426;