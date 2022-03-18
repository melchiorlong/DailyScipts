create table public.temp_ilrd_log_with_organic
(
	app_name varchar(256),
	kch_id varchar(256),
	ilrd_country varchar(256),
	rev_bj_date timestamp encode az64,
	fb_impr integer encode az64,
	ads_revenue_exclude_fb double precision
);

alter table public.temp_ilrd_log_with_organic owner to awsuser;

grant select on public.temp_ilrd_log_with_organic to gv_ro;

grant select on public.temp_ilrd_log_with_organic to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.temp_ilrd_log_with_organic to gv_online_rw;

grant select on public.temp_ilrd_log_with_organic to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.temp_ilrd_log_with_organic to gv_offline_rw;

grant select on public.temp_ilrd_log_with_organic to gv_alert;

grant select on public.temp_ilrd_log_with_organic to dev_user;

