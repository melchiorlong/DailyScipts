create table public.muid_dimension
(
	muid varchar(64),
	device_id varchar(64),
	app_name varchar(16),
	media_source varchar(64),
	kch_country varchar(32),
	kch_id varchar(64),
	app_install_version smallint encode az64,
	install_bj_datetime timestamp encode az64,
	country varchar(7)
);

alter table public.muid_dimension owner to awsuser;

grant select on public.muid_dimension to gv_ro;

grant select on public.muid_dimension to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.muid_dimension to gv_online_rw;

grant select on public.muid_dimension to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.muid_dimension to gv_offline_rw;

grant select on public.muid_dimension to gv_alert;

grant select on public.muid_dimension to dev_user;

