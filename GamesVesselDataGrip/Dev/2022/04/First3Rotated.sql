with ins_users   as (
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
     puzzle_temp as (
         select
             muid,
             is_rotated,
             trunc(convert_timezone('Asia/Shanghai', action_time))      as action_date,
             row_number() over (partition by muid order by action_time) as rn
         from puzzle_log
         where action_type = 1
           and trunc(convert_timezone('Asia/Shanghai', action_time)) <= '2022-03-31'
     ),
     muid        as (
         select
             ins.app_name,
             ins.ins_date,
             ins.device_model,
             md.muid
         from ins_users          ins
             join muid_dimension md
                  on ins.kch_id = md.kch_id
                      and md.app_name in ('aiolos_ip', 'aiolos_gp')
     ),
     lt          as (
         select
             puzzle_log.muid,
             count(distinct trunc(convert_timezone('Asia/Shanghai', action_time))) as act_cnt
         from puzzle_log
             join muid on puzzle_log.muid = muid.muid
         where datediff(day, ins_date, trunc(convert_timezone('Asia/Shanghai', action_time))) <= 60
           and datediff(day, ins_date, trunc(convert_timezone('Asia/Shanghai', action_time))) > 0
           and trunc(convert_timezone('Asia/Shanghai', action_time)) <= '2022-03-31'
         group by puzzle_log.muid
     ),
     temp_all    as (
         select
             puzzle_temp.muid,
             muid.app_name,
             muid.device_model,
             max(case when is_rotated = 'True' then 1 else 0 end)             as rotated,
             max(case when is_rotated = 'True' and rn <= 3 then 1 else 0 end) as rotated_3,
             sum(case when is_rotated <> 'True' then 0 else 1 end)            as rotated_no
         from puzzle_temp
             join muid on muid.muid = puzzle_temp.muid
         group by puzzle_temp.muid,
                  muid.app_name,
                  muid.device_model
     )
select
    muid.app_name,
    muid.device_model,
    count(distinct muid.muid)                                   as cnt,
    count(distinct case when rotated = 1 then muid.muid end)    as rotated_cnt,
    sum(case when rotated = 1 then lt.act_cnt end)              as rotated_lt60,
    1 + 1.0 * rotated_lt60 / rotated_cnt                        as rotated_lt,
    count(distinct case when rotated_3 = 1 then muid.muid end)  as rotated_3_cnt,
    sum(case when rotated_3 = 1 then lt.act_cnt end)            as rotated_3_lt60,
    1 + 1.0 * rotated_3_lt60 / rotated_3_cnt                    as rotated_3_lt,
    count(distinct case when rotated_no = 0 then muid.muid end) as rotated_no_cnt,
    sum(case when rotated_no = 0 then lt.act_cnt end)           as rotated_no_lt60,
    1 + 1.0 * rotated_no_lt60 / rotated_no_cnt                  as rotated_no_lt
from muid
    left join temp_all on muid.muid = temp_all.muid
    left join lt on temp_all.muid = lt.muid
group by muid.app_name,
         muid.device_model
order by app_name,
         device_model
;