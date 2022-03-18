create table public.temp_applovin_kch_install
(
	app_name varchar(12),
	muid varchar(64),
	kch_id varchar(64),
	country varchar(8),
	ins_date date encode az64
);

alter table public.temp_applovin_kch_install owner to awsuser;

grant select on public.temp_applovin_kch_install to gv_ro;

grant select on public.temp_applovin_kch_install to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.temp_applovin_kch_install to gv_online_rw;

grant select on public.temp_applovin_kch_install to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.temp_applovin_kch_install to gv_offline_rw;

grant select on public.temp_applovin_kch_install to gv_alert;

grant select on public.temp_applovin_kch_install to dev_user;

