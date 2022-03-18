create table public.ads_posd_kch_retention_activities
(
	muid varchar(64),
	install_date date encode az64,
	day_dimension integer encode az64,
	poseidon_active smallint encode az64,
	kch_active smallint encode az64
);

alter table public.ads_posd_kch_retention_activities owner to awsuser;

grant select on public.ads_posd_kch_retention_activities to gv_ro;

grant insert, select, update on public.ads_posd_kch_retention_activities to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.ads_posd_kch_retention_activities to gv_online_rw;

grant select on public.ads_posd_kch_retention_activities to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.ads_posd_kch_retention_activities to gv_offline_rw;

grant select on public.ads_posd_kch_retention_activities to gv_alert;

grant select on public.ads_posd_kch_retention_activities to dev_user;

