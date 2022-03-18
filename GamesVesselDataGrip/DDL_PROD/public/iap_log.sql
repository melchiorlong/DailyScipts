create table public.iap_log
(
	muid varchar(64),
	app_package_name varchar(64),
	platform varchar(32),
	app_version_code integer encode az64,
	country varchar(32),
	ip varchar(32),
	timezone double precision,
	user_segment varchar(32),
	action_time timestamp encode az64,
	action_type integer encode az64,
	device_id varchar(64),
	device_brand varchar(32),
	device_model varchar(32),
	os_version varchar(128),
	mb_source varchar(32),
	event varchar(32),
	product_id varchar(64),
	position varchar(32),
	service_log_time timestamp encode az64,
	log_date varchar(32),
	product_price double precision,
	activity_id varchar(255),
	activity_info varchar(255),
	consume_info varchar(255),
	iap_source varchar(255),
	raw_receipt_data varchar(65535),
	currency varchar(8)
);

alter table public.iap_log owner to gv_root;

grant select on public.iap_log to gv_ro;

grant select on public.iap_log to gv_online_ro;

grant select on public.iap_log to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.iap_log to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.iap_log to gv_offline_rw;

grant select on public.iap_log to metabase;

grant select on public.iap_log to gv_developer;

