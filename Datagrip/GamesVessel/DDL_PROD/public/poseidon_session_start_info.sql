create table public.poseidon_session_start_info
(
	log_date date,
	bj_date date encode az64,
	muid varchar(64)
)
sortkey(log_date);

alter table public.poseidon_session_start_info owner to gv_root;

grant select on public.poseidon_session_start_info to gv_ro;

grant select on public.poseidon_session_start_info to gv_online_ro;

grant select on public.poseidon_session_start_info to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_session_start_info to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.poseidon_session_start_info to gv_offline_rw;

grant select on public.poseidon_session_start_info to metabase;

grant select on public.poseidon_session_start_info to gv_developer;

