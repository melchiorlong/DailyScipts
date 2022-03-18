create table public.tmp_good30_rev
(
	muid varchar(64),
	country varchar(8),
	day0_rev double precision,
	day1_rev double precision,
	day2_rev double precision,
	day3_rev double precision,
	day4_rev double precision,
	day5_rev double precision,
	day6_rev double precision,
	day7_rev double precision
);

alter table public.tmp_good30_rev owner to gv_root;

grant select on public.tmp_good30_rev to gv_ro;

grant select on public.tmp_good30_rev to gv_online_ro;

grant select on public.tmp_good30_rev to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.tmp_good30_rev to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.tmp_good30_rev to gv_offline_rw;

grant select on public.tmp_good30_rev to metabase;

grant select on public.tmp_good30_rev to gv_developer;

