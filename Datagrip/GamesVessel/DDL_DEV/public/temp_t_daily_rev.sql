create table public.temp_t_daily_rev
(
	campaign_id varchar(64),
	country varchar(8),
	install_bj_date timestamp encode az64,
	rev_bj_date timestamp encode az64,
	fb_impr integer encode az64,
	ads_revenue_exclude_fb double precision,
	iap_rev double precision
);

alter table public.temp_t_daily_rev owner to awsuser;

grant select on public.temp_t_daily_rev to gv_ro;

grant select on public.temp_t_daily_rev to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.temp_t_daily_rev to gv_online_rw;

grant select on public.temp_t_daily_rev to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.temp_t_daily_rev to gv_offline_rw;

grant select on public.temp_t_daily_rev to gv_alert;

grant select on public.temp_t_daily_rev to dev_user;

