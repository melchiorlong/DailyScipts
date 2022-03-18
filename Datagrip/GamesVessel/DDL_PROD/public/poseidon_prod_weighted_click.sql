create table public.poseidon_prod_weighted_click
(
	create_date date not null,
	app_package_name varchar(256) not null,
	country varchar(32) not null,
	media_source varchar(64) not null,
	muid varchar(64) not null distkey,
	weighted_click integer not null encode az64,
	constraint poseidon_prod_weighted_click_pkey
		primary key (create_date, app_package_name, muid)
)
sortkey(create_date);

alter table public.poseidon_prod_weighted_click owner to gv_root;

grant select on public.poseidon_prod_weighted_click to gv_ro;

grant select on public.poseidon_prod_weighted_click to gv_online_ro;

grant select on public.poseidon_prod_weighted_click to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_prod_weighted_click to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.poseidon_prod_weighted_click to gv_offline_rw;

grant select on public.poseidon_prod_weighted_click to metabase;

grant select on public.poseidon_prod_weighted_click to gv_developer;

