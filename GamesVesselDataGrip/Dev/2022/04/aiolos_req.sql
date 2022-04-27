-- 标题：分别查一下
-- begin=0
-- 国家 US用户
-- 其他行为数据
-- 条件：Install Date：20211201 - 20220131
-- Session Date：20211201 - 20220331
-- 产品：Aiolos_gp / Aiolos_ip(Phone) / Aiolos_ip(Pad)


-- 1.验证2/3没有行为的用户 （ 关联不到puzzle log ）
-- ，在Poseidon上是否存在广告/session start等其他事件数据

with psd_act_muid as (
    select
        muid,
        sum(impr_cnt)            as impr_cnt_sum,
        sum(ban_cnt)             as ban_cnt_sum,
        sum(click_cnt)           as click_cnt_sum,
        sum(session_start_cnt)   as session_start_cnt_sum,
        sum(unban_cnt)           as unban_cnt_sum,
        sum(should_display_cnt)  as should_display_cnt_sum,
        (impr_cnt_sum + ban_cnt_sum + click_cnt_sum + session_start_cnt_sum + unban_cnt_sum +
         should_display_cnt_sum) as active_cnt
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
         where trunc(convert_timezone('Asia/Shanghai', action_time)) >= '2021-12-01'
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
    sum(case when pam.impr_cnt_sum > 0 then 1 else 0 end)           as psd_impr_cnt_sum,
    sum(case when pam.ban_cnt_sum > 0 then 1 else 0 end)            as psd_ban_cnt_sum,
    sum(case when pam.click_cnt_sum > 0 then 1 else 0 end)          as psd_click_cnt_sum,
    sum(case when pam.session_start_cnt_sum > 0 then 1 else 0 end)  as psd_session_start_cnt_sum,
    sum(case when pam.unban_cnt_sum > 0 then 1 else 0 end)          as psd_unban_cnt_sum,
    sum(case when pam.should_display_cnt_sum > 0 then 1 else 0 end) as psd_should_display_cnt_sum,
    sum(case when pam.active_cnt > 0 then 1 else 0 end)             as psd_active_cnt
from psd_act_muid        pam
    inner join ins_users iu
               on iu.muid = pam.muid
    left join  pz_log    pl
               on pl.muid = pam.muid
where pl.muid is null
group by iu.app_name,
         iu.device_model
;


-- 2.对1/3有行为数据的用户，统计其游戏内其他行为事件的人数：
-- 有topcard_show事件
-- 有image_show事件 -> action_type =show
-- 有topic_show事件
-- 有purchase事件
-- 有topic_click事件


with pz_log    as (
    select
        muid,
        count(case when action_type = 1 then 1 end)                          as begin_cnt,
        count(case when action_type = 7 then 1 end)                          as show_cnt,
        count(case when action_type = 8 then 1 end)                          as topic_show_cnt,
        count(case when action_type = 9 then 1 end)                          as topic_click_cnt,
        sum(case when location in ('TopCard', 'top_card') then 1 else 0 end) as top_card_cnt
    from puzzle_log
    where trunc(convert_timezone('Asia/Shanghai', action_time)) >= '2021-12-01'
      and trunc(convert_timezone('Asia/Shanghai', action_time)) <= '2022-03-31'
    group by muid
),
     ins_users as (
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
     iap_temp  as (
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
    sum(case when pl.show_cnt > 0 then 1 else 0 end)        as pl_show_cnt,
    sum(case when pl.topic_show_cnt > 0 then 1 else 0 end)  as pl_topic_show_cnt,
    sum(case when pl.topic_click_cnt > 0 then 1 else 0 end) as pl_topic_click_cnt,
    sum(case when pl.top_card_cnt > 0 then 1 else 0 end)    as pl_top_card_cnt,
    sum(case when nvl(it.iap_cnt, 0) > 0 then 1 else 0 end) as iap_cnt
from ins_users          iu
    inner join pz_log   pl
               on iu.muid = pl.muid
                   and pl.begin_cnt = 0
    left join  iap_temp it
               on it.muid = iu.muid
group by iu.app_name,
         iu.device_model
;


