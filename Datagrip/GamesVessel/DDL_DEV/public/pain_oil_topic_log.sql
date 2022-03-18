create table public.pain_oil_topic_log
(
	muid varchar(64),
	platform varchar(32),
	app_package_name varchar(64),
	app_version_code integer encode az64,
	country varchar(16),
	timezone real,
	user_segment varchar(32),
	action_time integer encode az64,
	painting_item_id varchar(64),
	topic_id varchar(64),
	thumb_id integer encode az64,
	action_type varchar(4),
	algo_version varchar(4),
	duration integer encode az64,
	ip varchar(32),
	log_date varchar(32)
);

alter table public.pain_oil_topic_log owner to awsuser;

grant select on public.pain_oil_topic_log to gv_ro;

grant select on public.pain_oil_topic_log to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.pain_oil_topic_log to gv_online_rw;

grant select on public.pain_oil_topic_log to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.pain_oil_topic_log to gv_offline_rw;

grant select on public.pain_oil_topic_log to gv_alert;

grant select on public.pain_oil_topic_log to dev_user;

