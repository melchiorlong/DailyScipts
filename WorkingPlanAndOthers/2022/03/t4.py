import datetime

def get_hour_range(hour_start, hour_end):
    """
    :return: 返回从hour_start到hour_end的所有小时的列表
    """
    dates = []
    dt = datetime.datetime.strptime(hour_start, "%Y-%m-%dT%H")
    dt_end = datetime.datetime.strptime(hour_end, "%Y-%m-%dT%H")
    while dt <= dt_end:
        dates.append(dt.strftime("%Y-%m-%dT%H"))
        dt = dt + datetime.timedelta(hours=1)
    return dates


hour_list = get_hour_range('2022-03-01T00', '2022-03-10T00')

for log_hour in hour_list:
    log_time = datetime.datetime.strptime(log_hour, "%Y-%m-%dT%H")

    log_table_query = """
                create temp table saori_log_temp as (
                    select
                        muid,
                        app_package_name,
                        app_version,
                        img_id,
                        country,
                        action_time,
                        action_type,
                        is_test,
                        img_thumb_index,
                        duration,
                        log_time
                    from spectrum.ods_gateway_saori_h
                    where 1 = 1
                      and log_time = '{exe_datetime}'
                );
            """.format(
                exe_datetime=log_time
            )
    print(log_table_query)
