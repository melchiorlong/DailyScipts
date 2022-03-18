create table public.user_event_log
(
	log_date varchar(16),
	action_type varchar(32),
	action_time timestamp encode az64,
	muid varchar(64),
	profile_id varchar(128),
	third_party_name varchar(32),
	fb_app_id varchar(32),
	facebook_id varchar(32),
	google_project_id varchar(32),
	google_id varchar(32),
	user_identifier varchar(64),
	user_name varchar(512),
	avatar varchar(2048),
	birthday varchar(32),
	email varchar(64),
	phone_number varchar(32),
	gender varchar(16),
	locale varchar(16),
	nickname varchar(512),
	full_name varchar(1024),
	dihck varchar(64),
	app_package_name varchar(64),
	app_version integer encode az64,
	device_type varchar(16),
	device_model varchar(16),
	device_os_version varchar(128),
	beje varchar(64),
	jegb varchar(64),
	jegw varchar(64),
	phone_brand varchar(128),
	screen_resolution varchar(64),
	country varchar(16),
	timezone double precision,
	language varchar(16),
	notify_token varchar(256),
	notify_setting varchar(16),
	ip varchar(64),
	muid_create_time timestamp encode az64,
	first_login varchar(8),
	avatar_url varchar(256),
	avatar_blob varchar(8),
	gjje varchar(255)
)
sortkey(log_date);

alter table public.user_event_log owner to gv_root;

grant select on public.user_event_log to gv_ro;

grant select on public.user_event_log to gv_online_ro;

grant select on public.user_event_log to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.user_event_log to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.user_event_log to gv_offline_rw;

grant select on public.user_event_log to metabase;

grant select on public.user_event_log to gv_developer;

