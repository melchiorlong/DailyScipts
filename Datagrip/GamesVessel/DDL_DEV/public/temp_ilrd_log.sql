create table public.temp_ilrd_log
(
	app_name varchar(256),
	kch_id varchar(256),
	ilrd_country varchar(256),
	rev_bj_date timestamp encode az64,
	fb_impr integer encode az64,
	ads_revenue_exclude_fb double precision
);

alter table public.temp_ilrd_log owner to awsuser;

grant select on public.temp_ilrd_log to gv_ro;

grant select on public.temp_ilrd_log to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.temp_ilrd_log to gv_online_rw;

grant select on public.temp_ilrd_log to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.temp_ilrd_log to gv_offline_rw;

grant select on public.temp_ilrd_log to gv_alert;

grant select on public.temp_ilrd_log to dev_user;

