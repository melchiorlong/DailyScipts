create table public.tmp_saori_ip_good30_ilrd_log
(
	muid varchar(64),
	bj_date date encode az64,
	fb_impr bigint encode az64,
	ads_revenue_exclude_fb double precision
);

alter table public.tmp_saori_ip_good30_ilrd_log owner to gv_root;

grant select on public.tmp_saori_ip_good30_ilrd_log to gv_ro;

grant select on public.tmp_saori_ip_good30_ilrd_log to gv_online_ro;

grant select on public.tmp_saori_ip_good30_ilrd_log to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.tmp_saori_ip_good30_ilrd_log to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.tmp_saori_ip_good30_ilrd_log to gv_offline_rw;

grant select on public.tmp_saori_ip_good30_ilrd_log to metabase;

grant select on public.tmp_saori_ip_good30_ilrd_log to gv_developer;

