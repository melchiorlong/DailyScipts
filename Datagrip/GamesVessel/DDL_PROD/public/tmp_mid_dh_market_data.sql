create table public.tmp_mid_dh_market_data
(
	date timestamp encode az64,
	country varchar(64),
	placement_name varchar(32),
	vendor varchar(32),
	res_id varchar(128),
	req bigint encode az64,
	fill bigint encode az64,
	impr bigint encode az64,
	click bigint encode az64,
	rev double precision,
	app_name varchar(32)
);

alter table public.tmp_mid_dh_market_data owner to gv_root;

grant select on public.tmp_mid_dh_market_data to gv_ro;

grant select on public.tmp_mid_dh_market_data to gv_online_ro;

grant select on public.tmp_mid_dh_market_data to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.tmp_mid_dh_market_data to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.tmp_mid_dh_market_data to gv_offline_rw;

grant select on public.tmp_mid_dh_market_data to metabase;

grant select on public.tmp_mid_dh_market_data to gv_developer;

