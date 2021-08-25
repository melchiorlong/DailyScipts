from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def db_conn():
    engine_PROD = create_engine('postgres://gv_developer:AjFtinLDMQ0w7i0f@3.230.194.153:5200/db_redshift_gv')
    dbsession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_PROD))
    return dbsession()


def balance_calc():
    balance_sql = """
        with muid_balance as (
        select trunc(action_time)                                                                                                              as action_time,
               muid,
               coin_change_type,
               coin_change_reason,
               first_value(current_value)
               over (partition by trunc(action_time), muid order by action_time desc rows between unbounded preceding and unbounded following) as balance
        from puzzle_log
        where platform = 'android'
          and coin_change_type is not null
          and trunc(action_time) <= '2021-07-01'
          and trunc(action_time) >= '2021-06-01'
    ),
         install_info as (
             select info.country_code,
                    info.date_occurred,
                    md.muid
             from kch_aiolos_gp_install_info info
                      inner join
                  muid_dimension md
                  on
                      info.kochava_device_id = md.kch_id
             where (country_code is not null or country_code <> '')
             and country_code in ('BR', 'MX', 'IN', 'AR', 'CO')
             and trunc(info.date_occurred) >= '2021-06-01'
             and trunc(info.date_occurred) <= '2021-07-01'
         ),
         balance_info_temp as (
             select distinct ins.country_code,
                    bal.muid,
                    trunc(ins.date_occurred) as date_occurred,
                    bal.balance              as balance
             from install_info ins
                      inner join
                  muid_balance bal
                  on
                          bal.muid = ins.muid
                          and bal.action_time = trunc(ins.date_occurred)
             where country_code is not null and country_code <> ''
         ),
         balance_info as (
             select ins.country_code,
                    trunc(ins.date_occurred)                                                     as date_occurred,
                    sum(case when trunc(ins.date_occurred) <= '2021-07-01' then ins.balance end) as day0_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-30' then ins.balance end) as day1_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-29' then ins.balance end) as day2_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-28' then ins.balance end) as day3_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-27' then ins.balance end) as day4_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-26' then ins.balance end) as day5_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-25' then ins.balance end) as day6_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-24' then ins.balance end) as day7_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-23' then ins.balance end) as day8_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-22' then ins.balance end) as day9_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-21' then ins.balance end) as day10_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-20' then ins.balance end) as day11_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-19' then ins.balance end) as day12_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-18' then ins.balance end) as day13_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-17' then ins.balance end) as day14_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-16' then ins.balance end) as day15_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-15' then ins.balance end) as day16_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-14' then ins.balance end) as day17_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-13' then ins.balance end) as day18_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-12' then ins.balance end) as day19_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-11' then ins.balance end) as day20_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-10' then ins.balance end) as day21_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-09' then ins.balance end) as day22_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-08' then ins.balance end) as day23_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-07' then ins.balance end) as day24_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-06' then ins.balance end) as day25_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-05' then ins.balance end) as day26_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-04' then ins.balance end) as day27_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-03' then ins.balance end) as day28_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-02' then ins.balance end) as day29_balance,
                    sum(case when trunc(ins.date_occurred) <= '2021-06-01' then ins.balance end) as day30_balance
             from balance_info_temp ins
             group by ins.country_code, trunc(ins.date_occurred)
         )
         -- balance_dws
             select country_code,
                    sum(nvl(day0_balance, 0))  as day0,
                    sum(nvl(day1_balance, 0))  as day1,
                    sum(nvl(day2_balance, 0))  as day2,
                    sum(nvl(day3_balance, 0))  as day3,
                    sum(nvl(day4_balance, 0))  as day4,
                    sum(nvl(day5_balance, 0))  as day5,
                    sum(nvl(day6_balance, 0))  as day6,
                    sum(nvl(day7_balance, 0))  as day7,
                    sum(nvl(day8_balance, 0))  as day8,
                    sum(nvl(day9_balance, 0))  as day9,
                    sum(nvl(day10_balance, 0)) as day10,
                    sum(nvl(day11_balance, 0)) as day11,
                    sum(nvl(day12_balance, 0)) as day12,
                    sum(nvl(day13_balance, 0)) as day13,
                    sum(nvl(day14_balance, 0)) as day14,
                    sum(nvl(day15_balance, 0)) as day15,
                    sum(nvl(day16_balance, 0)) as day16,
                    sum(nvl(day17_balance, 0)) as day17,
                    sum(nvl(day18_balance, 0)) as day18,
                    sum(nvl(day19_balance, 0)) as day19,
                    sum(nvl(day20_balance, 0)) as day20,
                    sum(nvl(day21_balance, 0)) as day21,
                    sum(nvl(day22_balance, 0)) as day22,
                    sum(nvl(day23_balance, 0)) as day23,
                    sum(nvl(day24_balance, 0)) as day24,
                    sum(nvl(day25_balance, 0)) as day25,
                    sum(nvl(day26_balance, 0)) as day26,
                    sum(nvl(day27_balance, 0)) as day27,
                    sum(nvl(day28_balance, 0)) as day28,
                    sum(nvl(day29_balance, 0)) as day29,
                    sum(nvl(day30_balance, 0)) as day30
             from balance_info
             group by country_code
        """
    conn_session = db_conn()
    try:
        balance_rs = conn_session.execute(balance_sql)
    except:
        conn_session.rollback()
        raise
    finally:
        conn_session.close()
    return balance_rs


def dnu_calc():
    balance_sql = """
            with muid_balance as (
            select trunc(action_time)                                                                                                              as action_time,
                   muid,
                   coin_change_type,
                   coin_change_reason,
                   first_value(current_value)
                   over (partition by trunc(action_time), muid order by action_time desc rows between unbounded preceding and unbounded following) as balance
            from puzzle_log
            where platform = 'android'
              and coin_change_type is not null
              and trunc(action_time) <= '2021-07-01'
              and trunc(action_time) >= '2021-06-01'
        ),
             install_info as (
                 select info.country_code,
                        info.date_occurred,
                        md.muid
                 from kch_aiolos_gp_install_info info
                          inner join
                      muid_dimension md
                      on
                          info.kochava_device_id = md.kch_id
                 where (country_code is not null or country_code <> '')
                 and country_code in ('BR', 'MX', 'IN', 'AR', 'CO')
                 and trunc(info.date_occurred) >= '2021-06-01'
                 and trunc(info.date_occurred) <= '2021-07-01'
             ),
             balance_info_temp as (
                 select distinct ins.country_code,
                        bal.muid,
                        trunc(ins.date_occurred) as date_occurred,
                        bal.balance              as balance
                 from install_info ins
                          inner join
                      muid_balance bal
                      on
                              bal.muid = ins.muid
                              and bal.action_time = trunc(ins.date_occurred)
                 where (country_code is not null or country_code <> '')
             ),
             dnu_info as (
         select ins.country_code,
                trunc(ins.date_occurred),
                sum(case when trunc(ins.date_occurred) <= '2021-07-01' then 1 else 0 end) as day0_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-30' then 1 else 0 end) as day1_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-29' then 1 else 0 end) as day2_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-28' then 1 else 0 end) as day3_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-27' then 1 else 0 end) as day4_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-26' then 1 else 0 end) as day5_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-25' then 1 else 0 end) as day6_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-24' then 1 else 0 end) as day7_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-23' then 1 else 0 end) as day8_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-22' then 1 else 0 end) as day9_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-21' then 1 else 0 end) as day10_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-20' then 1 else 0 end) as day11_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-19' then 1 else 0 end) as day12_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-18' then 1 else 0 end) as day13_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-17' then 1 else 0 end) as day14_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-16' then 1 else 0 end) as day15_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-15' then 1 else 0 end) as day16_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-14' then 1 else 0 end) as day17_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-13' then 1 else 0 end) as day18_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-12' then 1 else 0 end) as day19_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-11' then 1 else 0 end) as day20_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-10' then 1 else 0 end) as day21_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-09' then 1 else 0 end) as day22_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-08' then 1 else 0 end) as day23_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-07' then 1 else 0 end) as day24_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-06' then 1 else 0 end) as day25_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-05' then 1 else 0 end) as day26_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-04' then 1 else 0 end) as day27_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-03' then 1 else 0 end) as day28_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-02' then 1 else 0 end) as day29_dnu,
                sum(case when trunc(ins.date_occurred) <= '2021-06-01' then 1 else 0 end) as day30_dnu
         from install_info ins
         group by ins.country_code,
                  trunc(ins.date_occurred)
     )
      -- dnu_dws 
         select country_code,
                sum(nvl(day0_dnu, 0))  as day0,
                sum(nvl(day1_dnu, 0))  as day1,
                sum(nvl(day2_dnu, 0))  as day2,
                sum(nvl(day3_dnu, 0))  as day3,
                sum(nvl(day4_dnu, 0))  as day4,
                sum(nvl(day5_dnu, 0))  as day5,
                sum(nvl(day6_dnu, 0))  as day6,
                sum(nvl(day7_dnu, 0))  as day7,
                sum(nvl(day8_dnu, 0))  as day8,
                sum(nvl(day9_dnu, 0))  as day9,
                sum(nvl(day10_dnu, 0)) as day10,
                sum(nvl(day11_dnu, 0)) as day11,
                sum(nvl(day12_dnu, 0)) as day12,
                sum(nvl(day13_dnu, 0)) as day13,
                sum(nvl(day14_dnu, 0)) as day14,
                sum(nvl(day15_dnu, 0)) as day15,
                sum(nvl(day16_dnu, 0)) as day16,
                sum(nvl(day17_dnu, 0)) as day17,
                sum(nvl(day18_dnu, 0)) as day18,
                sum(nvl(day19_dnu, 0)) as day19,
                sum(nvl(day20_dnu, 0)) as day20,
                sum(nvl(day21_dnu, 0)) as day21,
                sum(nvl(day22_dnu, 0)) as day22,
                sum(nvl(day23_dnu, 0)) as day23,
                sum(nvl(day24_dnu, 0)) as day24,
                sum(nvl(day25_dnu, 0)) as day25,
                sum(nvl(day26_dnu, 0)) as day26,
                sum(nvl(day27_dnu, 0)) as day27,
                sum(nvl(day28_dnu, 0)) as day28,
                sum(nvl(day29_dnu, 0)) as day29,
                sum(nvl(day30_dnu, 0)) as day30
         from dnu_info
         group by country_code
            """
    conn_session = db_conn()
    try:
        # dnu_rs = offline_ro_session.execute(balance_sql)
        dnu_rs = conn_session.execute(balance_sql)
    except:
        conn_session.rollback()
        raise
    finally:
        conn_session.close()

    return dnu_rs


def median_calc():
    median_sql = """
            with muid_balance as (
            select trunc(action_time)                                                                                                              as action_time,
                   muid,
                   coin_change_type,
                   coin_change_reason,
                   first_value(current_value)
                   over (partition by trunc(action_time), muid order by action_time desc rows between unbounded preceding and unbounded following) as balance
            from puzzle_log
            where platform = 'android'
              and coin_change_type is not null
              and trunc(action_time) <= '2021-07-01'
              and trunc(action_time) >= '2021-06-01'
        ),
             install_info as (
                 select info.country_code,
                        info.date_occurred,
                        md.muid
                 from kch_aiolos_gp_install_info info
                          inner join
                      muid_dimension md
                      on
                          info.kochava_device_id = md.kch_id
                 where (country_code is not null or country_code <> '')
                 and country_code in ('BR', 'MX', 'IN', 'AR', 'CO')
                 and trunc(info.date_occurred) >= '2021-06-01'
                 and trunc(info.date_occurred) <= '2021-07-01'
             ),
             balance_info_temp as (
                 select distinct ins.country_code,
                        bal.muid,
                        trunc(ins.date_occurred) as date_occurred,
                        bal.balance              as balance
                 from install_info ins
                          inner join
                      muid_balance bal
                      on
                              bal.muid = ins.muid
                              and bal.action_time = trunc(ins.date_occurred)
                 where (country_code is not null or country_code <> '')
             ),
             balance_median_temp as (
         select bi.country_code,
                max(case when trunc(bi.date_occurred) <= '2021-07-01' then bi.balance else 0 end) as day0_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-30' then bi.balance else 0 end) as day1_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-29' then bi.balance else 0 end) as day2_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-28' then bi.balance else 0 end) as day3_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-27' then bi.balance else 0 end) as day4_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-26' then bi.balance else 0 end) as day5_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-25' then bi.balance else 0 end) as day6_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-24' then bi.balance else 0 end) as day7_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-23' then bi.balance else 0 end) as day8_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-22' then bi.balance else 0 end) as day9_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-21' then bi.balance else 0 end) as day10_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-20' then bi.balance else 0 end) as day11_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-19' then bi.balance else 0 end) as day12_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-18' then bi.balance else 0 end) as day13_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-17' then bi.balance else 0 end) as day14_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-16' then bi.balance else 0 end) as day15_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-15' then bi.balance else 0 end) as day16_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-14' then bi.balance else 0 end) as day17_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-13' then bi.balance else 0 end) as day18_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-12' then bi.balance else 0 end) as day19_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-11' then bi.balance else 0 end) as day20_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-10' then bi.balance else 0 end) as day21_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-09' then bi.balance else 0 end) as day22_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-08' then bi.balance else 0 end) as day23_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-07' then bi.balance else 0 end) as day24_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-06' then bi.balance else 0 end) as day25_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-05' then bi.balance else 0 end) as day26_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-04' then bi.balance else 0 end) as day27_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-03' then bi.balance else 0 end) as day28_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-02' then bi.balance else 0 end) as day29_balance,
                max(case when trunc(bi.date_occurred) <= '2021-06-01' then bi.balance else 0 end) as day30_balance
         from balance_info_temp bi
         group by bi.country_code, bi.muid, trunc(bi.date_occurred)
     )
      -- median_dws 
         select country_code,
                median(day0_balance) over (partition by country_code)  as day0,
                median(day1_balance) over (partition by country_code)  as day1,
                median(day2_balance) over (partition by country_code)  as day2,
                median(day3_balance) over (partition by country_code)  as day3,
                median(day4_balance) over (partition by country_code)  as day4,
                median(day5_balance) over (partition by country_code)  as day5,
                median(day6_balance) over (partition by country_code)  as day6,
                median(day7_balance) over (partition by country_code)  as day7,
                median(day8_balance) over (partition by country_code)  as day8,
                median(day9_balance) over (partition by country_code)  as day9,
                median(day10_balance) over (partition by country_code) as day10,
                median(day11_balance) over (partition by country_code) as day11,
                median(day12_balance) over (partition by country_code) as day12,
                median(day13_balance) over (partition by country_code) as day13,
                median(day14_balance) over (partition by country_code) as day14,
                median(day15_balance) over (partition by country_code) as day15,
                median(day16_balance) over (partition by country_code) as day16,
                median(day17_balance) over (partition by country_code) as day17,
                median(day18_balance) over (partition by country_code) as day18,
                median(day19_balance) over (partition by country_code) as day19,
                median(day20_balance) over (partition by country_code) as day20,
                median(day21_balance) over (partition by country_code) as day21,
                median(day22_balance) over (partition by country_code) as day22,
                median(day23_balance) over (partition by country_code) as day23,
                median(day24_balance) over (partition by country_code) as day24,
                median(day25_balance) over (partition by country_code) as day25,
                median(day26_balance) over (partition by country_code) as day26,
                median(day27_balance) over (partition by country_code) as day27,
                median(day28_balance) over (partition by country_code) as day28,
                median(day29_balance) over (partition by country_code) as day29,
                median(day30_balance) over (partition by country_code) as day30
         from balance_median_temp
            """
    conn_session = db_conn()
    try:
        # dnu_rs = offline_ro_session.execute(balance_sql)
        median_rs = conn_session.execute(median_sql)
    except:
        conn_session.rollback()
        raise
    finally:
        conn_session.close()

    return median_rs


def session_execute(balance_rs=None, dnu_rs=None, median_rs=None):
    balance_dict = {}
    dnu_dict = {}
    median_dict = {}

    result_dict = {}
    for r in balance_rs:
        country = r[0]
        balance_info = {}
        for cnt in range(31):
            # balance_info['day' + str(cnt)] = {'balance': r[cnt + 1]}
            result_dict.setdefault(country, {})
            result_dict[country]['day' + str(cnt)].setdefault('balance', {'balance': r[cnt + 1]})

    for r in dnu_rs:
        country = r[0]
        dnu_info = {}
        for cnt in range(31):
            # dnu_info['day' + str(cnt)] = r[cnt + 1]
            result_dict.setdefault(country, {})
            result_dict[country]['day' + str(cnt)].setdefault('dnu', {'dnu': r[cnt + 1]})
        # dnu_dict[country] = dnu_info

    for r in median_rs:
        country = r[0]
        median_info = {}
        for cnt in range(31):
            # median_info['day' + str(cnt)] = r[cnt + 1]
        # median_dict[country] = median_info
            result_dict.setdefault(country, {})
            result_dict[country]['day' + str(cnt)].setdefault('median', {'median': r[cnt + 1]})



    print(balance_dict)
    print(dnu_dict)
    print(median_dict)

if __name__ == '__main__':
    balance_rs = balance_calc()
    dnu_rs = dnu_calc()
    median_rs = median_calc()
    session_execute(balance_rs, dnu_rs, median_rs)
