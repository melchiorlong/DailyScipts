import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import DML, Keyword

query = """
with creawler_table as (
    select
        trunc(dateadd(hour, 8, date)) as bj_date,
        placement_name,
        sum(impr)                     as sum_impr
    from mid_dh_market_data
    where app_name = 'saori_ip'
      and dateadd(hour, 8, date) >= '2022-03-01'
      and dateadd(hour, 8, date) <= '2022-03-17'
    group by placement_name,
             bj_date
),
     psd_log        as (
         select
             trunc(dateadd(hour, 8, service_log_time))                          as bj_date,
             placement_name,
             sum(case when action_type = 'impression' then 1 else 0 end)        as sum_impr,
             sum(case when action_type = 'ad_should_display' then 1 else 0 end) as sum_ad_should_display,
             sum(case
                     when action_type = 'impression' and app_version_code > 28
                         then 1
                         else 0 end)                                            as sum_impression_Max
         from spectrum.fact_ivt_poseidon_log log
         where 1 = 1
           and action_type in ('impression', 'ad_should_display')
           and dateadd(hour, 8, log_time) >= '2022-03-01'
           and trunc(dateadd(hour, 8, service_log_time)) >= '2022-03-01'
           and trunc(dateadd(hour, 8, service_log_time)) <= '2022-03-17'
           and app_package_name = 'art.color.planet.paint.by.number.game.puzzle'
         group by bj_date,
                  placement_name
     )
select
    pl.bj_date,
    pl.placement_name,
    ct.sum_impr              as CrawlerTask_Impression,
    pl.sum_impr              as PSD_LOG_Impression,
    pl.sum_ad_should_display as PSD_LOG_ad_should_display,
    pl.sum_impression_Max    as PSD_LOG_Impression_Max
from creawler_table    ct
    inner join psd_log pl
               on ct.placement_name = pl.placement_name
                   and ct.bj_date = pl.bj_date
order by pl.bj_date,
         pl.placement_name
;




"""




ALL_JOIN_TYPE = ('LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'FULL JOIN', 'LEFT OUTER JOIN', 'FULL OUTER JOIN')


def is_subselect(parsed):
    """
    是否子查询
    :param parsed: T.Token
    """
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == 'SELECT':
            return True
    return False


def extract_from_part(parsed):
    """
    提取from之后模块
    """
    from_seen = False
    for item in parsed.tokens:
        if from_seen:
            if is_subselect(item):
                for x in extract_from_part(item):
                    yield x
            elif item.ttype is Keyword:
                from_seen = False
                continue
            else:
                yield item
        elif item.ttype is Keyword and item.value.upper() == 'FROM':
            from_seen = True


def extract_join_part(parsed):
    """
    提取join之后模块
    """
    flag = False
    for item in parsed.tokens:
        if flag:
            if item.ttype is Keyword:
                flag = False
                continue
            else:
                yield item
        if item.ttype is Keyword and item.value.upper() in ALL_JOIN_TYPE:
            flag = True


def extract_table_identifiers(token_stream):
    for item in token_stream:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                yield identifier.get_name()
        elif isinstance(item, Identifier):
            yield item.get_name()
        elif item.ttype is Keyword:
            yield item.value


def extract_tables(sql):
    """
    提取sql中的表名（select语句）
    """
    from_stream = extract_from_part(sqlparse.parse(sql)[0])
    join_stream = extract_join_part(sqlparse.parse(sql)[0])
    return list(extract_table_identifiers(from_stream)) + list(extract_table_identifiers(join_stream))


print(extract_tables(query))
