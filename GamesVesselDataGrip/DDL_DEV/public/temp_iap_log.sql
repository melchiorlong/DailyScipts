create table public.temp_iap_log
(
	app_name varchar(16),
	rev_bj_date date encode az64,
	kch_id varchar(64),
	iap_rev double precision
);

alter table public.temp_iap_log owner to awsuser;

grant select on public.temp_iap_log to gv_ro;

grant select on public.temp_iap_log to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.temp_iap_log to gv_online_rw;

grant select on public.temp_iap_log to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.temp_iap_log to gv_offline_rw;

grant select on public.temp_iap_log to gv_alert;

grant select on public.temp_iap_log to dev_user;

