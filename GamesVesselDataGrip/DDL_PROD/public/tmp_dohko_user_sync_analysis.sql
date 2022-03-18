create table public.tmp_dohko_user_sync_analysis
(
	muid varchar(64),
	app_package_name varchar(64),
	platform varchar(16),
	app_version_code integer encode az64,
	country varchar(8),
	user_segment varchar(32),
	ip varchar(64),
	timezone double precision,
	algo_version varchar(16),
	action_type varchar(16),
	marketing_name varchar(64),
	network_status varchar(16),
	log_time timestamp encode az64,
	bj_action_time timestamp encode az64,
	bj_start timestamp encode az64,
	bj_end timestamp encode az64
);

alter table public.tmp_dohko_user_sync_analysis owner to gv_root;

grant select on public.tmp_dohko_user_sync_analysis to gv_ro;

grant select on public.tmp_dohko_user_sync_analysis to gv_online_ro;

grant select on public.tmp_dohko_user_sync_analysis to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.tmp_dohko_user_sync_analysis to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.tmp_dohko_user_sync_analysis to gv_offline_rw;

grant select on public.tmp_dohko_user_sync_analysis to metabase;

grant select on public.tmp_dohko_user_sync_analysis to gv_developer;

