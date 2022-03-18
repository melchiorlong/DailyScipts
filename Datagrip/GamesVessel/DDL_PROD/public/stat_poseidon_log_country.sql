create table public.stat_poseidon_log_country
(
	country varchar(8)
);

alter table public.stat_poseidon_log_country owner to gv_root;

grant select on public.stat_poseidon_log_country to gv_ro;

grant select on public.stat_poseidon_log_country to gv_online_ro;

grant select on public.stat_poseidon_log_country to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.stat_poseidon_log_country to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.stat_poseidon_log_country to gv_offline_rw;

grant select on public.stat_poseidon_log_country to metabase;

grant select on public.stat_poseidon_log_country to gv_developer;

