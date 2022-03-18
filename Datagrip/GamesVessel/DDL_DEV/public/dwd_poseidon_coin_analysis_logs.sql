create table public.dwd_poseidon_coin_analysis_logs
(
	app_name varchar(9),
	app_version_code integer encode az64,
	country varchar(64),
	action_time timestamp encode az64,
	muid varchar(64),
	coin_change_reason varchar(64),
	previous_value integer encode az64,
	current_value integer encode az64,
	coin_change_type integer encode az64
);

alter table public.dwd_poseidon_coin_analysis_logs owner to awsuser;

grant select on public.dwd_poseidon_coin_analysis_logs to gv_ro;

grant select on public.dwd_poseidon_coin_analysis_logs to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.dwd_poseidon_coin_analysis_logs to gv_online_rw;

grant select on public.dwd_poseidon_coin_analysis_logs to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.dwd_poseidon_coin_analysis_logs to gv_offline_rw;

grant select on public.dwd_poseidon_coin_analysis_logs to gv_alert;

grant select on public.dwd_poseidon_coin_analysis_logs to dev_user;

