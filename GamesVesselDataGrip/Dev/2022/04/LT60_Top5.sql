-- * 区分 Aiolos_ip iPhone / Aiolos_ip iPad / Aiolos_gp 这三坨新用户，
-- 每一坨中 LT60 最好的 5% 的用户（按每个用户的前 60 天有过事件的天数倒序），的
-- DNU 数量，
-- 平均 LT60，
-- 用过旋转开局的用户占比，
-- 以及旋转开局占总开局数占比；


with ins_users          as (
    -- long
    select distinct
        app_name,
        case when app_name = 'aiolos_gp' then 'android' else device_model end as device_model,
        kch.kochava_device_id                                                 as kch_id,
        trunc(kch.bj_date_occurred)                                           as ins_date
    from dwd_ua_kch_install_info kch
    where ins_date >= '2021-12-01'
      and ins_date <= '2022-01-31'
      and country_code = 'US'
      and (app_name = 'aiolos_gp' or (app_name = 'aiolos_ip' and device_model in ('iPhone', 'iPad')))
),
     ins_md_temp        as (
         select distinct
             md.muid,
             ins.app_name,
             ins.device_model,
             trunc(md.install_bj_datetime) as ins_date
         from ins_users                ins
             inner join muid_dimension md
                        on ins.kch_id = md.kch_id
         where md.app_name in ('aiolos_gp', 'aiolos_ip')
     ),
     puzzle_temp        as (
         select
             imt.muid,
             imt.app_name,
             imt.device_model,
             pl.action_type,
             nvl(datediff(days, imt.ins_date, dateadd(hour, 8, pl.action_time)), 0) as date_diff,
             case when is_rotated = 'True' then 1 else 0 end                        as is_rotated_flag
         from puzzle_log            pl
             right join ins_md_temp imt
                        on pl.muid = imt.muid
                            and trunc(convert_timezone('Asia/Shanghai', action_time)) <= '2022-03-31'
     ),
     active_temp        as (
         select
             muid,
             app_name,
             device_model,
             count(distinct date_diff) as lt_days
         from puzzle_temp
         where date_diff <= 60
         group by muid,
                  app_name,
                  device_model
     ),
     lt_5_perscent_temp as (
         select
             muid,
             app_name,
             device_model,
             lt_days,
             percent_rank
         from (
             select
                 muid,
                 app_name,
                 device_model,
                 lt_days,
                 percent_rank()
                 over (partition by app_name, device_model order by lt_days desc) as percent_rank
             from active_temp
         ) rank_temp
         where rank_temp.percent_rank <= 0.05
     ),
     lt_5_muid          as (
         select
             app_name,
             device_model,
             avg(lt_days) as avg_lt
         from lt_5_perscent_temp
         where lt_days > 0
         group by app_name,
                  device_model
     ),
     condition_temp     as (
         select
             pt.muid,
             pt.app_name,
             pt.device_model,
             sum(is_rotated_flag)   as life_rotated,
             count(is_rotated_flag) as all_games_cnt
         from puzzle_temp                  pt
             inner join lt_5_perscent_temp l5pt
                        on l5pt.muid = pt.muid
         where action_type = 1
         group by pt.muid,
                  pt.app_name,
                  pt.device_model
     ),
     res_temp           as (
         select
             ct.app_name,
             ct.device_model,
             l6t.avg_lt,
             sum(ct.all_games_cnt)                                       as all_games_cnt,
             count(distinct case when life_rotated > 0 then ct.muid end) as at_least_rotated_cnt,
             sum(life_rotated)                                           as rotated_begin_cnt
         from condition_temp      ct
             inner join lt_5_muid l6t
                        on l6t.app_name = ct.app_name
                            and l6t.device_model = ct.device_model
         group by ct.app_name,
                  ct.device_model,
                  l6t.avg_lt
     )
select *
from res_temp
;

