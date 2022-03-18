create table public.retention_rate_dohkoip
(
	campaign_id varchar(64),
	country_code varchar(8),
	install_date timestamp encode az64,
	media_source varchar(64),
	team varchar(64),
	optimizer varchar(256)
);

alter table public.retention_rate_dohkoip owner to gv_ro;

