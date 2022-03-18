create view public.test1(trunc, media_source, campaign_id, country_code, count) as
	CREATE MATERIALIZED VIEW test1 AUTO REFRESH YES AS

select TRUNC(dateadd(hour, 8, date_occurred)),
       (case when media_source is null then 'null' else media_source end),
       (case when campaign_id is null then 'null' else campaign_id end),
       (case when country_code is null then 'null' else country_code end),
       count(distinct kochava_device_id)
from kch_saori_gp_install_info
group by TRUNC(dateadd(hour, 8, date_occurred)),
         media_source,
         campaign_id,
         country_code;

alter table public.test1 owner to gv_ro;

