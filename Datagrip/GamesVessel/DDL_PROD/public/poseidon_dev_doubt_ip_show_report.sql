create table public.poseidon_dev_doubt_ip_show_report
(
	ip varchar(64) not null
		constraint poseidon_dev_doubt_ip_show_report_pkey
			primary key,
	device_count integer not null encode az64,
	ban_device_count integer not null encode az64,
	muid_count integer not null encode az64,
	ban_muid_count integer not null encode az64,
	organic integer not null encode az64,
	facebook integer not null encode az64,
	google integer not null encode az64,
	unity integer not null encode az64,
	applovin integer not null encode az64,
	ironsource integer not null encode az64,
	apple integer not null encode az64,
	unknown integer not null encode az64,
	total_weighted_click integer not null encode az64
);

alter table public.poseidon_dev_doubt_ip_show_report owner to gv_root;

grant select on public.poseidon_dev_doubt_ip_show_report to gv_ro;

grant select on public.poseidon_dev_doubt_ip_show_report to gv_online_ro;

grant select on public.poseidon_dev_doubt_ip_show_report to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_dev_doubt_ip_show_report to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.poseidon_dev_doubt_ip_show_report to gv_offline_rw;

grant select on public.poseidon_dev_doubt_ip_show_report to metabase;

grant select on public.poseidon_dev_doubt_ip_show_report to gv_developer;

