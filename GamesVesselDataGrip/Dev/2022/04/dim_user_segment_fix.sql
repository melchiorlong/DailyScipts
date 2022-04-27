-- 备份
create table temp_dim_user_segment_backup_20220419 as
select *
from dim_user_segment;

-- 建临时表
drop table if exists temp_user_segment_saga_fix;
create table temp_user_segment_saga_fix as
select
    spectrum_log.muid,
    spectrum_log.user_segment,
    trunc(CONVERT_TIMEZONE('UTC', 'Asia/Shanghai', min(spectrum_log.action_time))) as action_bj_date
from muid_dimension               as muid_dim
    inner join ods_gateway_saga_d as spectrum_log
               on muid_dim.muid = spectrum_log.muid
                   and muid_dim.app_name in ('saga_gp', 'saga_ip')
group by spectrum_log.muid,
         spectrum_log.user_segment
;

-- 删除 temp_user_segment_saga_fix.action_bj_date >= dim_user_segment.action_bj_date
delete
from temp_user_segment_saga_fix
    using
        dim_user_segment
where temp_user_segment_saga_fix.muid = dim_user_segment.muid
  and temp_user_segment_saga_fix.user_segment = dim_user_segment.user_segment
  and temp_user_segment_saga_fix.action_bj_date >= dim_user_segment.action_bj_date;

-- 删除 dim_user_segment.action_bj_date > temp_user_segment_saga_fix.action_bj_date
delete
from dim_user_segment
    using
        temp_user_segment_saga_fix
where temp_user_segment_saga_fix.muid = dim_user_segment.muid
  and temp_user_segment_saga_fix.user_segment = dim_user_segment.user_segment
  and dim_user_segment.action_bj_date > temp_user_segment_saga_fix.action_bj_date;

-- 保留的为 每个muid 每个user_segment 下的 最小action_bj_date
insert into dim_user_segment(muid,
                             user_segment,
                             action_bj_date)
select
    muid,
    user_segment,
    action_bj_date
from temp_user_segment_saga_fix;



select
    action_bj_date,
    count(1)
from dim_user_segment
where action_bj_date <= '2022-04-18'
group by action_bj_date
order by action_bj_date desc
;
select
    action_bj_date,
    count(1)
from temp_dim_user_segment_backup_20220419
where action_bj_date <= '2022-04-18'
group by action_bj_date
order by action_bj_date desc
;







