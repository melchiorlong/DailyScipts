create table public.mv_tbl__tickets_mv__0
(
	media_source varchar(32),
	stat_kch_install_retention_count_oid bigint encode az64 distkey,
	num_rec integer encode az64
)
diststyle key;

alter table public.mv_tbl__tickets_mv__0 owner to rdsdb;

