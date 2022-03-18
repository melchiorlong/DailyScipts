create table public.test_sorted_date_process
(
	campaign_id varchar(64),
	day_time timestamp
)
sortkey(day_time);

alter table public.test_sorted_date_process owner to gv_ro;

