create table public.temp_applovin_saori_log
(
	muid varchar(64),
	action_date date encode az64,
	is_active integer encode az64,
	complete_count bigint encode az64,
	hint_count bigint encode az64
);

alter table public.temp_applovin_saori_log owner to awsuser;

grant select on public.temp_applovin_saori_log to gv_ro;

grant select on public.temp_applovin_saori_log to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.temp_applovin_saori_log to gv_online_rw;

grant select on public.temp_applovin_saori_log to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.temp_applovin_saori_log to gv_offline_rw;

grant select on public.temp_applovin_saori_log to gv_alert;

grant select on public.temp_applovin_saori_log to dev_user;

