create table public.mid_ilrd_should_display
(
	bj_date date encode az64,
	app_name varchar(16),
	country varchar(8),
	placement varchar(16),
	should_display bigint encode az64,
	impr bigint encode az64
);

alter table public.mid_ilrd_should_display owner to gv_root;

grant select on public.mid_ilrd_should_display to gv_ro;

grant select on public.mid_ilrd_should_display to gv_online_ro;

grant select on public.mid_ilrd_should_display to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_should_display to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_should_display to gv_offline_rw;

grant select on public.mid_ilrd_should_display to metabase;

grant select on public.mid_ilrd_should_display to gv_developer;

