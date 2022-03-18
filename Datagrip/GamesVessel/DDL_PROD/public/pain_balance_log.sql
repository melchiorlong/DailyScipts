create table public.pain_balance_log
(
	muid varchar(64),
	platform varchar(16),
	app_package_name varchar(64),
	app_version_code integer encode az64,
	country varchar(8),
	timezone double precision,
	user_segment varchar(32),
	action_time bigint encode az64,
	painting_item_id varchar(64),
	topic_id varchar(64),
	action_type varchar(16),
	previous_balance integer encode az64,
	current_balance integer encode az64,
	ip varchar(32),
	log_date varchar(16)
);

alter table public.pain_balance_log owner to gv_root;

grant select on public.pain_balance_log to gv_ro;

grant select on public.pain_balance_log to gv_online_ro;

grant select on public.pain_balance_log to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.pain_balance_log to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.pain_balance_log to gv_offline_rw;

grant select on public.pain_balance_log to metabase;

grant select on public.pain_balance_log to gv_developer;

