create temp table pain_oil_enable_log as (
    select
        muid,
        app_package_name,
        app_version_code,
        painting_item_id,
        country,
        action_time,
        trunc(dateadd(sec, action_time, '1970-01-01'))::varchar(10) as action_date,
        action_type,
        is_test,
        duration,
        algo_version,
        log_time
    from spectrum.fact_pain_dohko_log
    where trunc(log_time) >= '2022-02-28'
      and is_zeus = 1);



create temp table pain_oil_other_stat_table as (
    select
        app_package_name,
        app_version_code,
        painting_item_id                                                            as item_id,
        country,
        algo_version,
        action_date,
        sum(case action_type when '1' then 1 else 0 end)                            as begin_count,
        sum(case action_type when '2' then 1 else 0 end)                            as complete_count,
        sum(case action_type when '0' then 1 else 0 end)                            as unknown_count,
        sum(case action_type when '3' then 1 else 0 end)                            as replay_count,
        sum(case action_type when '5' then 1 else 0 end)                            as hint_count,
        sum(case action_type when '4' then 1 else 0 end)                            as show_count,
        sum(case when action_type = '4' and is_test = 'True' then 1 else 0 end)     as show_recommend_count,
        sum(case when action_type = '1' and is_test = 'True' then 1 else 0 end)     as begin_recommend_count,
        sum(case when action_type = '2' and duration != 0 then duration else 0 end) as duration_sum,
        sum(case when action_type = '2' and duration != 0 then 1 else 0 end)        as duration_count
    from pain_oil_enable_log
    where action_date >= '2022-02-28'
      and action_date < '2022-03-18'
    group by item_id,
             app_package_name,
             app_version_code,
             country,
             algo_version,
             action_date);



create temp table pain_oil_another_play_table as (
    with query_table    as (
        select
            action_time,
            action_date,
            action_type,
            painting_item_id as item_id,
            app_package_name,
            app_version_code,
            muid,
            country,
            algo_version
        from pain_oil_enable_log
        where action_date >= '2022-02-28'
          and action_date < '2022-03-18'
          and action_type in ('1', '2', '3')
    ),
         complete_table as (
             select
                 action_time,
                 item_id,
                 app_package_name,
                 app_version_code,
                 muid,
                 country,
                 algo_version
             from query_table
             where action_type = '2'
         ),
         tmp_table      as (
             select
                 complete_table.item_id          as item_id,
                 complete_table.app_package_name as app_package_name,
                 complete_table.app_version_code as app_version_code,
                 complete_table.muid             as muid,
                 complete_table.country          as country,
                 complete_table.action_time      as action_time,
                 complete_table.algo_version     as algo_version,
                 min(query_table.action_time)    as next_action_time
             from query_table
                 inner join complete_table
                            on query_table.muid = complete_table.muid
                                and query_table.action_time - complete_table.action_time > 0
                                and query_table.action_time - complete_table.action_time < 600
             group by complete_table.item_id,
                      complete_table.app_package_name,
                      complete_table.app_version_code,
                      complete_table.muid,
                      complete_table.country,
                      complete_table.action_time,
                      complete_table.algo_version
         ),
         res_table      as (
             select
                 tmp_table.item_id          as item_id,
                 tmp_table.app_package_name as app_package_name,
                 tmp_table.app_version_code as app_version_code,
                 tmp_table.muid             as muid,
                 tmp_table.country          as country,
                 tmp_table.action_time      as action_time,
                 query_table.action_date,
                 tmp_table.algo_version     as algo_version
             from tmp_table
                 inner join query_table
                            on tmp_table.muid = query_table.muid
                                and tmp_table.next_action_time = query_table.action_time
                                and query_table.action_type in ('1', '3')
         )
    select
        action_date,
        item_id,
        app_package_name,
        app_version_code,
        country,
        algo_version,
        count(distinct muid) as another_play_count
    from res_table
    group by item_id,
             app_package_name,
             app_version_code,
             country,
             algo_version,
             action_date
);



create temp table stat_oilpainting_image_summary_temp as (
    select
        pain_oil_other_stat_table.action_date,
        pain_oil_other_stat_table.app_package_name      as app_package_name,
        pain_oil_other_stat_table.app_version_code      as app_version_code,
        pain_oil_other_stat_table.item_id               as item_id,
        pain_oil_other_stat_table.country               as country,
        pain_oil_other_stat_table.begin_count           as begin_count,
        pain_oil_other_stat_table.complete_count        as complete_count,
        pain_oil_other_stat_table.unknown_count         as unknown_count,
        pain_oil_other_stat_table.replay_count          as replay_count,
        pain_oil_another_play_table.another_play_count  as another_play_count,
        pain_oil_other_stat_table.hint_count            as hint_count,
        pain_oil_other_stat_table.show_count            as show_count,
        pain_oil_other_stat_table.show_recommend_count  as show_recommend_count,
        pain_oil_other_stat_table.begin_recommend_count as begin_recommend_count,
        pain_oil_other_stat_table.duration_sum          as duration_sum,
        pain_oil_other_stat_table.duration_count        as duration_count,
        pain_oil_other_stat_table.algo_version          as algo_version
    from pain_oil_other_stat_table
        left join pain_oil_another_play_table
                  on pain_oil_other_stat_table.app_package_name = pain_oil_another_play_table.app_package_name
                      and pain_oil_other_stat_table.app_version_code = pain_oil_another_play_table.app_version_code
                      and pain_oil_other_stat_table.item_id = pain_oil_another_play_table.item_id
                      and pain_oil_other_stat_table.country = pain_oil_another_play_table.country
                      and pain_oil_other_stat_table.algo_version = pain_oil_another_play_table.algo_version
                      and pain_oil_other_stat_table.action_date = pain_oil_another_play_table.action_date
);



delete
from stat_oilpainting_image_summary using stat_oilpainting_image_summary_temp as stage
where stat_oilpainting_image_summary.action_date = stage.action_date
  and stat_oilpainting_image_summary.app_package_name = stage.app_package_name
  and stat_oilpainting_image_summary.app_version_code = stage.app_version_code
  and stat_oilpainting_image_summary.item_id = stage.item_id
  and stat_oilpainting_image_summary.country = stage.country
  and stat_oilpainting_image_summary.algo_version = stage.algo_version;



insert
into stat_oilpainting_image_summary (action_date,
                                     app_package_name,
                                     app_version_code,
                                     item_id,
                                     country,
                                     begin_count,
                                     complete_count,
                                     unknown_count,
                                     replay_count,
                                     another_play_count,
                                     hint_count,
                                     show_count,
                                     show_recommend_count,
                                     begin_recommend_count,
                                     duration_sum,
                                     duration_count,
                                     algo_version)
select
    action_date,
    app_package_name,
    app_version_code,
    item_id,
    country,
    begin_count,
    complete_count,
    unknown_count,
    replay_count,
    (case
         when another_play_count
             then another_play_count
             else
             0
        end) as another_play_count,
    hint_count,
    show_count,
    show_recommend_count,
    begin_recommend_count,
    duration_sum,
    duration_count,
    algo_version
from stat_oilpainting_image_summary_temp;



drop table pain_oil_other_stat_table;
drop table pain_oil_another_play_table;
drop table stat_oilpainting_image_summary_temp
