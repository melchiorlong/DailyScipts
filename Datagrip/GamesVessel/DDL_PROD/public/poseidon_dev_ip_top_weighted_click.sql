create table public.poseidon_dev_ip_top_weighted_click
(
	create_date date not null encode az64,
	ip varchar(64) not null,
	constraint poseidon_dev_ip_top_weighted_click_pkey
		primary key (create_date, ip)
);

alter table public.poseidon_dev_ip_top_weighted_click owner to gv_root;

grant select on public.poseidon_dev_ip_top_weighted_click to gv_ro;

grant select on public.poseidon_dev_ip_top_weighted_click to gv_online_ro;

grant select on public.poseidon_dev_ip_top_weighted_click to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_dev_ip_top_weighted_click to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.poseidon_dev_ip_top_weighted_click to gv_offline_rw;

grant select on public.poseidon_dev_ip_top_weighted_click to metabase;

grant select on public.poseidon_dev_ip_top_weighted_click to gv_developer;

