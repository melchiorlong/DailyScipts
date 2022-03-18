create table public.poseidon_muid_app_mapper
(
	muid varchar(64),
	app_package_name varchar(64)
)
sortkey(muid);

alter table public.poseidon_muid_app_mapper owner to gv_root;

grant select on public.poseidon_muid_app_mapper to gv_ro;

grant select on public.poseidon_muid_app_mapper to gv_online_ro;

grant select on public.poseidon_muid_app_mapper to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_muid_app_mapper to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.poseidon_muid_app_mapper to gv_offline_rw;

grant select on public.poseidon_muid_app_mapper to metabase;

grant select on public.poseidon_muid_app_mapper to gv_developer;

