create table public.test_sorted_auto
(
	campaign_id varchar(64),
	day_time timestamp encode az64
);

alter table public.test_sorted_auto owner to gv_ro;

