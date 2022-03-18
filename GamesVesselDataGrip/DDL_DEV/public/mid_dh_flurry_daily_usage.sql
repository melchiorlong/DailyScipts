create table public.mid_dh_flurry_daily_usage
(
	date timestamp encode az64,
	app_name varchar(16),
	country varchar(8),
	dau_flurry integer encode az64,
	dnu_flurry integer encode az64
);

alter table public.mid_dh_flurry_daily_usage owner to awsuser;

grant select on public.mid_dh_flurry_daily_usage to gv_ro;

grant select on public.mid_dh_flurry_daily_usage to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.mid_dh_flurry_daily_usage to gv_online_rw;

grant select on public.mid_dh_flurry_daily_usage to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_dh_flurry_daily_usage to gv_offline_rw;

grant select on public.mid_dh_flurry_daily_usage to gv_alert;

grant select on public.mid_dh_flurry_daily_usage to dev_user;

