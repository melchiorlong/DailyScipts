create table public.dim_poseidon_market_meta
(
	vendor varchar(32),
	ad_resource_id varchar(128),
	placement_name varchar(32),
	app_name varchar(32)
)
sortkey(vendor, ad_resource_id);

alter table public.dim_poseidon_market_meta owner to gv_root;

grant select on public.dim_poseidon_market_meta to gv_ro;

grant select on public.dim_poseidon_market_meta to gv_online_ro;

grant select on public.dim_poseidon_market_meta to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.dim_poseidon_market_meta to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.dim_poseidon_market_meta to gv_offline_rw;

grant select on public.dim_poseidon_market_meta to metabase;

