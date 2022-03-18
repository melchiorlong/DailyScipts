create table public.retention_aiolos_gp
(
	campaignid varchar(64),
	country_code varchar(8),
	dt date encode az64,
	media_source varchar(64),
	team varchar(64),
	optimizer varchar(256),
	total_install_user bigint encode az64,
	retention_day1 bigint encode az64,
	retention_day2 bigint encode az64,
	retention_day7 bigint encode az64,
	retention_day30 bigint encode az64
);

alter table public.retention_aiolos_gp owner to gv_ro;

