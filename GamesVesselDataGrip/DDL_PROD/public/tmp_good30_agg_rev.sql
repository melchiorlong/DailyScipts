create table public.tmp_good30_agg_rev
(
	muid varchar(64),
	country varchar(8),
	come_bj_date date encode az64,
	daydiff bigint encode az64,
	bj_date date encode az64,
	rev double precision
);

alter table public.tmp_good30_agg_rev owner to gv_root;

grant select on public.tmp_good30_agg_rev to gv_ro;

grant select on public.tmp_good30_agg_rev to gv_online_ro;

grant select on public.tmp_good30_agg_rev to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.tmp_good30_agg_rev to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.tmp_good30_agg_rev to gv_offline_rw;

grant select on public.tmp_good30_agg_rev to metabase;

grant select on public.tmp_good30_agg_rev to gv_developer;

