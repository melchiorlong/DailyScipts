create table public.stat_poseidon_log_au
(
	utc_date date,
	app_package_name varchar(64),
	kch_country varchar(8),
	media_source varchar(64),
	user_segment varchar(32),
	muid varchar(64)
)
sortkey(utc_date, app_package_name, kch_country);

alter table public.stat_poseidon_log_au owner to gv_root;

grant select on public.stat_poseidon_log_au to gv_ro;

grant select on public.stat_poseidon_log_au to gv_online_ro;

grant select on public.stat_poseidon_log_au to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.stat_poseidon_log_au to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.stat_poseidon_log_au to gv_offline_rw;

grant select on public.stat_poseidon_log_au to metabase;

grant select on public.stat_poseidon_log_au to gv_developer;

