create table public.saga_log
(
	log_date varchar(16),
	muid varchar(64),
	app_package_name varchar(64),
	platform varchar(16),
	app_version_code integer encode az64,
	country varchar(64),
	action_time timestamp encode az64,
	ip varchar(64),
	timezone double precision,
	user_segment varchar(32),
	action_type varchar(32),
	bgs_status varchar(8),
	vibration_status varchar(8),
	position varchar(32),
	restart_times integer encode az64,
	level integer encode az64,
	block_count integer encode az64,
	exp integer encode az64,
	revive_times integer encode az64,
	score integer encode az64,
	is_new_record varchar(8),
	highest_record integer encode az64,
	duration_list varchar(256),
	highest_num integer encode az64,
	reward_value integer encode az64,
	previous_coin_value integer encode az64,
	current_coin_value integer encode az64,
	coin_change_type integer encode az64,
	coin_change_reason varchar(8),
	hammer_times integer encode az64
)
sortkey(action_time);

alter table public.saga_log owner to awsuser;

grant select on public.saga_log to gv_ro;

grant select on public.saga_log to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.saga_log to gv_online_rw;

grant select on public.saga_log to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.saga_log to gv_offline_rw;

grant select on public.saga_log to gv_alert;

grant select on public.saga_log to dev_user;

