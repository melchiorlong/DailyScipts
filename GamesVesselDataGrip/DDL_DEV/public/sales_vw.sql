create view public.sales_vw(campaign_id, day_time) as
	SELECT test_sorted_auto.campaign_id, test_sorted_auto.day_time
FROM test_sorted_auto
UNION ALL
SELECT test_no_sorted.campaign_id, test_no_sorted.day_time
FROM test_no_sorted;

alter table public.sales_vw owner to gv_ro;

