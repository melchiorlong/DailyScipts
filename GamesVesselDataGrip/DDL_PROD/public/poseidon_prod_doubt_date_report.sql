create table public.poseidon_prod_doubt_date_report
(
	query_date date not null,
	app_package_name varchar(256) not null,
	country varchar(32) not null,
	ip varchar(64) not null,
	device_count integer not null encode az64,
	ban_device_count integer not null encode az64,
	muid_count integer not null encode az64,
	ban_muid_count integer not null encode az64,
	total_weighted_click integer not null encode az64,
	constraint poseidon_prod_doubt_date_report_pkey
		primary key (query_date, app_package_name, country, ip)
)
sortkey(query_date);

alter table public.poseidon_prod_doubt_date_report owner to gv_root;

grant select on public.poseidon_prod_doubt_date_report to gv_ro;

grant select on public.poseidon_prod_doubt_date_report to gv_online_ro;

grant select on public.poseidon_prod_doubt_date_report to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_prod_doubt_date_report to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.poseidon_prod_doubt_date_report to gv_offline_rw;

grant select on public.poseidon_prod_doubt_date_report to metabase;

grant select on public.poseidon_prod_doubt_date_report to gv_developer;

