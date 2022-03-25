select
            date,
            case right(app_name, 2)
                when 'gp' then 'android'
                when 'ip' then 'iOS'
            end as platform,
            app_name,
            country,
            vendor as network,
            dh_adunit_id as adunit_id,
            dh_adunit_name as adunit_name,
            placement_name as adplacement_name,
            bank_info,
            account_id,
            sum(req)         as ad_requests,
            sum(fill)        as matched_requests,
            sum(impr)        as impressions,
            sum(click)       as clicks,
            sum(rev)         as earnings,
            'USD' as currency,
            trunc(getdate()) as row_created,
            trunc(getdate()) as row_updated
        from
            mid_dh_market_data
        where
            trunc(date) = '2022-03-22'
        group by date,
                 platform,
                 app_name,
                 country,
                 vendor,
                 dh_adunit_id,
                 dh_adunit_name,
                 placement_name,
                 bank_info,
                 account_id,
                 currency,
                 row_created,
                 row_updated;



select distinct
trunc(date)
from mid_dh_market_data
where account_id is not null;




select
distinct account_id
from mid_dh_market_data