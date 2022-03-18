create table public.poseidon_click_info
(
	log_date date,
	muid varchar(64),
	placement_name varchar(64),
	vendor varchar(64),
	action_id varchar(64)
)
sortkey(log_date);

alter table public.poseidon_click_info owner to gv_root;

grant select on public.poseidon_click_info to gv_ro;

grant select on public.poseidon_click_info to gv_online_ro;

grant select on public.poseidon_click_info to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_click_info to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.poseidon_click_info to gv_offline_rw;

grant select on public.poseidon_click_info to metabase;

grant select on public.poseidon_click_info to gv_developer;

