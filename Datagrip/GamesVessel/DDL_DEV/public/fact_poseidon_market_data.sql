create table public.fact_poseidon_market_data
(
	date timestamp,
	vendor varchar(32),
	ad_resource_id varchar(128),
	country varchar(64),
	placement_name varchar(32),
	app_name varchar(32),
	req bigint encode az64,
	fill bigint encode az64,
	impr bigint encode az64,
	click bigint encode az64,
	rev double precision
)
sortkey(date, vendor, ad_resource_id, country);

alter table public.fact_poseidon_market_data owner to awsuser;

grant select on public.fact_poseidon_market_data to gv_ro;

grant select on public.fact_poseidon_market_data to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.fact_poseidon_market_data to gv_online_rw;

grant select on public.fact_poseidon_market_data to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.fact_poseidon_market_data to gv_offline_rw;

grant select on public.fact_poseidon_market_data to gv_alert;

grant select on public.fact_poseidon_market_data to dev_user;

