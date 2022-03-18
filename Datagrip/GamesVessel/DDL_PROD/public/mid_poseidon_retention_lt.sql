create table public.mid_poseidon_retention_lt
(
	date timestamp encode az64,
	app_name varchar(16),
	country varchar(8),
	team varchar(16),
	optimizer varchar(32),
	media_source varchar(32),
	retention37_1d integer encode az64,
	retention37_7d integer encode az64,
	retention37_30d integer encode az64,
	install37_1d integer encode az64,
	install37_7d integer encode az64,
	install37_30d integer encode az64,
	lt37_30d double precision,
	lt37_60d double precision,
	lt37_90d double precision,
	lt37_180d double precision,
	lt37_360d double precision,
	coefficient37_a double precision,
	coefficient37_b double precision,
	retention14_1d integer encode az64,
	retention14_2d integer encode az64,
	retention14_3d integer encode az64,
	retention14_7d integer encode az64,
	install14_1d integer encode az64,
	install14_2d integer encode az64,
	install14_3d integer encode az64,
	install14_7d integer encode az64,
	retention120_1d integer encode az64,
	retention120_7d integer encode az64,
	retention120_30d integer encode az64,
	retention120_60d integer encode az64,
	retention120_90d integer encode az64,
	install120_1d integer encode az64,
	install120_7d integer encode az64,
	install120_30d integer encode az64,
	install120_60d integer encode az64,
	install120_90d integer encode az64,
	install37_1d_muid integer encode az64,
	install37_7d_muid integer encode az64,
	install37_30d_muid integer encode az64,
	retention37_1d_muid integer encode az64,
	retention37_7d_muid integer encode az64,
	retention37_30d_muid integer encode az64,
	install14_1d_muid integer encode az64,
	install14_2d_muid integer encode az64,
	install14_3d_muid integer encode az64,
	install14_7d_muid integer encode az64,
	retention14_1d_muid integer encode az64,
	retention14_2d_muid integer encode az64,
	retention14_3d_muid integer encode az64,
	retention14_7d_muid integer encode az64
);

alter table public.mid_poseidon_retention_lt owner to gv_root;

grant select on public.mid_poseidon_retention_lt to gv_ro;

grant select on public.mid_poseidon_retention_lt to gv_online_ro;

grant select on public.mid_poseidon_retention_lt to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_poseidon_retention_lt to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.mid_poseidon_retention_lt to gv_offline_rw;

grant select on public.mid_poseidon_retention_lt to metabase;

grant select on public.mid_poseidon_retention_lt to gv_developer;

