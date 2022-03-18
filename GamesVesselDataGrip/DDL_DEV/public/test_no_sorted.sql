create table public.test_no_sorted
(
	campaign_id varchar(64),
	day_time timestamp encode az64
);

alter table public.test_no_sorted owner to gv_ro;

