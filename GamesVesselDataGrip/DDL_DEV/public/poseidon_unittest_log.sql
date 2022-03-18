create table public.poseidon_unittest_log
(
	log_date varchar(16),
	muid varchar(64),
	app_package_name varchar(64),
	platform varchar(16),
	app_version_code integer encode az64,
	country varchar(8),
	timezone double precision,
	network_type varchar(32),
	action_time timestamp encode az64,
	action_type varchar(16),
	action_id varchar(64),
	placement_name varchar(64),
	vendor varchar(64),
	ad_format varchar(64),
	ad_id varchar(80),
	ip varchar(64),
	service_log_time timestamp encode az64,
	local_datetime timestamp encode az64,
	user_segment varchar(32),
	code integer encode az64,
	size integer encode az64,
	log_time timestamp encode az64
);

alter table public.poseidon_unittest_log owner to awsuser;

grant select on public.poseidon_unittest_log to gv_ro;

grant select on public.poseidon_unittest_log to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_unittest_log to gv_online_rw;

grant select on public.poseidon_unittest_log to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_unittest_log to gv_offline_rw;

grant select on public.poseidon_unittest_log to gv_alert;

grant select on public.poseidon_unittest_log to dev_user;

