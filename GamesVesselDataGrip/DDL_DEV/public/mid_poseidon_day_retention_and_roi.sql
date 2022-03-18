create table public.mid_poseidon_day_retention_and_roi
(
	app_name varchar(16) not null,
	country varchar(64) not null,
	date timestamp not null encode az64,
	team varchar(64) not null,
	optimizer varchar(256) not null,
	media_source varchar(64) not null,
	spend double precision,
	kch_nu integer encode az64,
	kch_recovery_period integer encode az64,
	dh_nu integer encode az64,
	dh_recovery_period integer encode az64,
	avg_arpdau double precision,
	retention_1d integer encode az64,
	install_1d integer encode az64,
	retention_2d integer encode az64,
	install_2d integer encode az64,
	retention_3d integer encode az64,
	install_3d integer encode az64,
	retention_7d integer encode az64,
	install_7d integer encode az64,
	media_source_retention_7d integer encode az64,
	media_source_install_7d integer encode az64,
	media_source_lt_30d double precision,
	coefficient_a double precision,
	coefficient_b double precision,
	retention_review smallint encode az64,
	kch_nu_muid integer encode az64,
	retention_1d_muid integer encode az64,
	retention_2d_muid integer encode az64,
	retention_3d_muid integer encode az64,
	retention_7d_muid integer encode az64,
	install_1d_muid integer encode az64,
	install_2d_muid integer encode az64,
	install_3d_muid integer encode az64,
	install_7d_muid integer encode az64
);

alter table public.mid_poseidon_day_retention_and_roi owner to awsuser;

grant select on public.mid_poseidon_day_retention_and_roi to gv_ro;

grant select on public.mid_poseidon_day_retention_and_roi to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.mid_poseidon_day_retention_and_roi to gv_online_rw;

grant select on public.mid_poseidon_day_retention_and_roi to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_poseidon_day_retention_and_roi to gv_offline_rw;

grant select on public.mid_poseidon_day_retention_and_roi to gv_alert;

grant select on public.mid_poseidon_day_retention_and_roi to dev_user;

