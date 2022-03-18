create table public.muid_info
(
	muid varchar(255) distkey,
	dihck varchar(255),
	app_package_name varchar(255),
	app_version integer encode az64,
	device_type varchar(255),
	device_model varchar(255),
	device_os_version varchar(255),
	beje varchar(255),
	jegb varchar(255),
	jegw varchar(255),
	country varchar(255),
	language varchar(255),
	timezone double precision,
	notify_token varchar(255),
	notify_setting integer encode az64,
	gjje varchar(255),
	ip varchar(255),
	create_time bigint encode az64,
	update_time bigint encode az64,
	profile_id varchar(255)
)
sortkey(gjje);

alter table public.muid_info owner to gv_root;

grant select on public.muid_info to gv_ro;

grant select on public.muid_info to gv_online_ro;

grant select on public.muid_info to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.muid_info to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.muid_info to gv_offline_rw;

grant select on public.muid_info to metabase;

grant select on public.muid_info to gv_developer;

