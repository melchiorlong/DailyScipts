create table public.mv_tbl__test1__0
(
	trunc date encode az64,
	media_source varchar(64),
	campaign_id varchar(64),
	country_code varchar(8),
	count bigint encode az64
);

alter table public.mv_tbl__test1__0 owner to rdsdb;

