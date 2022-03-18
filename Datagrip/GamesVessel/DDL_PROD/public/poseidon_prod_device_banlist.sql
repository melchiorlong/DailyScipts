create table public.poseidon_prod_device_banlist
(
	ban_date date not null,
	device_id varchar(64) not null,
	reason smallint not null encode az64,
	duration integer not null encode az64,
	constraint poseidon_prod_device_banlist_pkey
		primary key (ban_date, device_id, reason)
)
sortkey(ban_date);

alter table public.poseidon_prod_device_banlist owner to gv_root;

grant select on public.poseidon_prod_device_banlist to gv_ro;

grant select on public.poseidon_prod_device_banlist to gv_online_ro;

grant select on public.poseidon_prod_device_banlist to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_prod_device_banlist to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.poseidon_prod_device_banlist to gv_offline_rw;

grant select on public.poseidon_prod_device_banlist to metabase;

grant select on public.poseidon_prod_device_banlist to gv_developer;

