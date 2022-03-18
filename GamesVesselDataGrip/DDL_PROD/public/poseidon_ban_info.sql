create table public.poseidon_ban_info
(
	log_date date,
	muid varchar(64),
	code integer encode az64,
	size integer encode az64
)
sortkey(log_date);

alter table public.poseidon_ban_info owner to gv_root;

grant select on public.poseidon_ban_info to gv_ro;

grant select on public.poseidon_ban_info to gv_online_ro;

grant select on public.poseidon_ban_info to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_ban_info to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.poseidon_ban_info to gv_offline_rw;

grant select on public.poseidon_ban_info to metabase;

grant select on public.poseidon_ban_info to gv_developer;

