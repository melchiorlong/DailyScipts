from datetime import datetime, timedelta, date

class IlrdDataUpdate:

    _date_start = date(2021, 6, 1)
    _date_end = date(2021, 7, 26)

    def data_update(self):
        for i in range((self._date_end - self._date_start).days + 1):
            day = self._date_start + timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            sql_statament = """
                update mid_ilrd_quality_check_dau
                    set mid_ilrd_quality_check_dau.ads_dau = temp.ads_dau
                from (
                    select trunc(dateadd(hour, 8, service_log_time)) as bj_date,
                        (case app_package_name
                            when 'art.color.planet.oil.paint.canvas.number' then 'dohko_ip'
                            when 'art.color.planet.oil.paint.canvas.number.free' then 'dohko_gp'
                            when 'art.color.planet.paint.by.number.game.puzzle.free' then 'saori_gp'
                            when 'art.color.planet.paint.by.number.game.puzzle' then 'saori_ip'
                            when 'art.color.planet.jigsaw.puzzle.online.free' then 'aiolos_gp'
                            when 'art.color.planet.jigsaw.puzzle.online' then 'aiolos_ip'
                            when 'happy.puzzle.merge.block.shoot2048.number.game.free' then 'saga_gp'
                            else 'null' end)                     as app_name,
                            country,
                        count(distinct case
                                   when (app_package_name = 'art.color.planet.oil.paint.canvas.number' and
                                         app_version_code >= 3) or
                                        (app_package_name = 'art.color.planet.oil.paint.canvas.number.free' and
                                         app_version_code >= 2) or
                                        (app_package_name = 'art.color.planet.paint.by.number.game.puzzle.free' and
                                         app_version_code >= 2) or
                                        (app_package_name = 'art.color.planet.paint.by.number.game.puzzle' and
                                         app_version_code >= 2) or
                                        (app_package_name = 'art.color.planet.jigsaw.puzzle.online.free' and
                                         app_version_code >= 6) or
                                        (app_package_name = 'art.color.planet.jigsaw.puzzle.online' and
                                         app_version_code >= 5) or
                                        (app_package_name = 'happy.puzzle.merge.block.shoot2048.number.game.free' and
                                         app_version_code >= 4) then muid
                                   else null end)         as ads_dau
                    from 
                        spectrum.fact_ivt_poseidon_log
                    where 
                        datediff(
                        hour,
                        '{day_str}',
                        dateadd(hour, 8, log_time)
                        ) between -1 and 24
                        and trunc(dateadd(hour, 8, service_log_time)) = '{day_str}'
                        and app_package_name in
                        ('art.color.planet.oil.paint.canvas.number', 'art.color.planet.oil.paint.canvas.number.free',
                        'art.color.planet.paint.by.number.game.puzzle.free',
                        'art.color.planet.paint.by.number.game.puzzle', 'art.color.planet.jigsaw.puzzle.online.free',
                        'art.color.planet.jigsaw.puzzle.online',
                        'happy.puzzle.merge.block.shoot2048.number.game.free')
                    group by 
                        trunc(dateadd(hour, 8, service_log_time)),
                        country,
                        app_package_name
                ) temp
        where bj_date = '{day_str}'
            and mid_ilrd_quality_check_dau.app_name = temp.app_name
            and mid_ilrd_quality_check_dau.country = temp.country;
                    """.format(
                day_str=day_str
            )

            print(sql_statament)


if __name__ == '__main__':
        app = IlrdDataUpdate()
        app.data_update()