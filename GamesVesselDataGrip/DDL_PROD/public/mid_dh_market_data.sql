create table public.mid_dh_market_data
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
	rev double precision,
	bank_info varchar(32),
	dh_adunit_id varchar(128),
	dh_adunit_name varchar(128)
)
sortkey(date, vendor, ad_resource_id, country);

alter table public.mid_dh_market_data owner to gv_root;

grant select on public.mid_dh_market_data to gv_ro;

grant select on public.mid_dh_market_data to gv_online_ro;

grant select on public.mid_dh_market_data to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_dh_market_data to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.mid_dh_market_data to gv_offline_rw;

grant select on public.mid_dh_market_data to metabase;

grant select on public.mid_dh_market_data to gv_developer;

