create table public.poseidon_dev_ip_whitelist
(
	create_date date not null encode az64,
	creator varchar(64) not null,
	ip varchar(64) not null,
	constraint poseidon_dev_ip_whitelist_pkey
		primary key (create_date, creator, ip)
);

alter table public.poseidon_dev_ip_whitelist owner to gv_root;

grant select on public.poseidon_dev_ip_whitelist to gv_ro;

grant select on public.poseidon_dev_ip_whitelist to gv_online_ro;

grant select on public.poseidon_dev_ip_whitelist to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_dev_ip_whitelist to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.poseidon_dev_ip_whitelist to gv_offline_rw;

grant select on public.poseidon_dev_ip_whitelist to metabase;

grant select on public.poseidon_dev_ip_whitelist to gv_developer;

