create table public.mv_tbl__tick__0
(
	a1 varchar(32),
	a2 varchar(32),
	a3 integer encode az64,
	test_oid bigint encode az64 distkey,
	num_rec integer encode az64
)
diststyle key;

alter table public.mv_tbl__tick__0 owner to rdsdb;

