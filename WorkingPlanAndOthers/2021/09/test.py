
class CampaignDetail2MidTotalRev:

    def __init__(self, date):
        # self.redshift_session = offline_rw_session
        self.date = date

    day_dimension_list = [0, 1, 2, 3, 7, 14, 30, 45, 60, 120, 180, 360]

    def _table_trans(self):
        """
        此方法为使 dws_ua_muid_campaign_detail 表兼容原 mid_ilrd_campaign_roi_total_rev 表
        按照 campaign_id, rev_bj_date, country 聚合
        分别计算 day_dimension = [0，1, 2, 3, 7, 14, 30, 45, 60, 120, 180, 360] 的
        ads_rev, iap_rev, ads_rev_include_fb
        并将计算结果插至 mid_ilrd_campaign_roi_total_rev 中
        """

        day_dimension_list = [0, 1, 2, 3, 7, 14, 30, 45, 60, 120, 180, 360]

        rev_sql_factor = ",".join([f"""
                        sum((case
                                 when dumcd.day_dimension <= {d}
                                     then dumcd.ads_rev_without_fb
                                     else 0 end)
                            +
                            (case
                                 when tc.fb_cpm is not null
                                     and dumcd.day_dimension <= {d}
                                     then dumcd.facebook_ads_impr_cnt * tc.fb_cpm
                                     else 0 end))                                               as day{d}_ads_rev,
                        sum(case when dumcd.day_dimension <= {d} then dumcd.iap_rev else 0 end)   as day{d}_iap_rev,
                        min(case
                                when dumcd.day_dimension <= {d} and tc.fb_cpm is null
                                    then 'false'
                                    else 'true' end)                                            as day{d}_ads_rev_include_fb
            """ for d in day_dimension_list])

        update_sql_factor = ",".join(
            [f"""
            day{d}_ads_rev = temp_total_rev.day{d}_ads_rev
            """ for d in day_dimension_list]
        )

        insert_sql_factor = ",".join(
            [f"""
            day{d}_ads_rev, day{d}_iap_rev, day{d}_ads_rev_include_fb
            """ for d in day_dimension_list]
        )

        trans_sql = """
            create temp table temp_total_rev as (
                with temp_cpm as (
                    select distinct
                        trunc(convert_timezone('Asia/Shanghai', date)) as cpm_date,
                        app_name,
                        country,
                        fb_cpm
                    from mid_ilrd_dh_fb_cpm
                    where dateadd(day, 360, cpm_date) >= '{execute_date}'
                )
                select
                    -- dumcd.ua_media                                                          as ua_media,
                    dumcd.campaign_id                                                       as campaign_id,
                    dumcd.country                                                           as country,
                    dumcd.install_bj_date                                                   as bj_date,
                    {rev_sql_factor}
                from dws_ua_muid_campaign_detail dumcd
                    left join temp_cpm           tc
                              on dumcd.rev_bj_date = tc.cpm_date
                                  and tc.country   = dumcd.country
                                  and tc.app_name  = dumcd.app_name
                where 1 = 1
                  and dumcd.install_bj_date is not null
                  and dumcd.campaign_id <> ''
                  and trunc(dateadd(day, 390, dumcd.install_bj_date)) >= '{execute_date}'
                group by dumcd.campaign_id,
                         dumcd.install_bj_date,
                         dumcd.country
                         -- ,dumcd.ua_media
            );

            -- merge into mid_ilrd_campaign_roi_total_rev 表

            update mid_ilrd_campaign_roi_total_rev
            set {update_sql_factor}
            from temp_total_rev
            where mid_ilrd_campaign_roi_total_rev.campaign_id = temp_total_rev.campaign_id
              and mid_ilrd_campaign_roi_total_rev.country = temp_total_rev.country
              and mid_ilrd_campaign_roi_total_rev.bj_date = temp_total_rev.bj_date;

            delete
            from temp_total_rev
                using mid_ilrd_campaign_roi_total_rev
            where mid_ilrd_campaign_roi_total_rev.campaign_id = temp_total_rev.campaign_id
              and mid_ilrd_campaign_roi_total_rev.country     = temp_total_rev.country
              and mid_ilrd_campaign_roi_total_rev.bj_date     = temp_total_rev.bj_date;

            insert into mid_ilrd_campaign_roi_total_rev (campaign_id, country, bj_date, 
            {insert_sql_factor}
                                                         )
            select
                campaign_id,
                country,
                bj_date,
                {insert_sql_factor}
            from temp_total_rev;

            -- 清理临时表
            drop table temp_total_rev;
        """.format(
            execute_date=self.date,
            rev_sql_factor=rev_sql_factor,
            update_sql_factor=update_sql_factor,
            insert_sql_factor=insert_sql_factor,
        )
        print(trans_sql)

    def task_run(self):
        self._table_trans()

app = CampaignDetail2MidTotalRev('2021-09-01')
app.task_run()