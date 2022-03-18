create table public.poseidon_muid_ip_mapper
(
	log_date date not null,
	muid varchar(64) not null distkey,
	ip varchar(64) not null,
	constraint poseidon_muid_ip_mapper_pkey
		primary key (log_date, muid, ip)
)
sortkey(log_date);

alter table public.poseidon_muid_ip_mapper owner to gv_root;

grant select on public.poseidon_muid_ip_mapper to gv_ro;

grant select on public.poseidon_muid_ip_mapper to gv_online_ro;

grant select on public.poseidon_muid_ip_mapper to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_muid_ip_mapper to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.poseidon_muid_ip_mapper to gv_offline_rw;

grant select on public.poseidon_muid_ip_mapper to metabase;

grant select on public.poseidon_muid_ip_mapper to gv_developer;

