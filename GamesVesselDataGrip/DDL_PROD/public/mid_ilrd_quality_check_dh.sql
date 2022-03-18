create table public.mid_ilrd_quality_check_dh
(
	date date encode az64,
	app_name varchar(16),
	country varchar(64),
	ad_format varchar(64),
	network varchar(32),
	rev double precision,
	impr bigint encode az64,
	fb_rev double precision
);

alter table public.mid_ilrd_quality_check_dh owner to gv_offline_rw;

grant select on public.mid_ilrd_quality_check_dh to gv_ro;

grant select on public.mid_ilrd_quality_check_dh to gv_online_ro;

grant select on public.mid_ilrd_quality_check_dh to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_quality_check_dh to gv_online_rw;

grant select on public.mid_ilrd_quality_check_dh to metabase;

grant select on public.mid_ilrd_quality_check_dh to gv_developer;

