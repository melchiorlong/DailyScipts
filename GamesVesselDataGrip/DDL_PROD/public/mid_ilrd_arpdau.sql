create table public.mid_ilrd_arpdau
(
	bj_date date encode az64,
	app_name varchar(16),
	media_source varchar(64),
	country varchar(8),
	fb_dau bigint encode az64,
	total_dau bigint encode az64,
	fb_impr bigint encode az64,
	ads_revenue_exclude_fb double precision
);

alter table public.mid_ilrd_arpdau owner to gv_offline_rw;

grant select on public.mid_ilrd_arpdau to gv_ro;

grant select on public.mid_ilrd_arpdau to gv_online_ro;

grant select on public.mid_ilrd_arpdau to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_arpdau to gv_online_rw;

grant select on public.mid_ilrd_arpdau to metabase;

grant select on public.mid_ilrd_arpdau to gv_developer;

