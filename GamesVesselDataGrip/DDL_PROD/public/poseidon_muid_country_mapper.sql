create table public.poseidon_muid_country_mapper
(
	log_date date,
	muid varchar(64),
	country varchar(64)
)
sortkey(log_date);

alter table public.poseidon_muid_country_mapper owner to gv_root;

grant select on public.poseidon_muid_country_mapper to gv_ro;

grant select on public.poseidon_muid_country_mapper to gv_online_ro;

grant select on public.poseidon_muid_country_mapper to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_muid_country_mapper to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.poseidon_muid_country_mapper to gv_offline_rw;

grant select on public.poseidon_muid_country_mapper to metabase;

grant select on public.poseidon_muid_country_mapper to gv_developer;

