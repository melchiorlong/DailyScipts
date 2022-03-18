create table public.mid_poseidon_day_ad_revenue
(
	app_name varchar(16) not null,
	country varchar(64) not null,
	date date not null encode az64,
	vendor varchar(64) not null,
	placement_name varchar(64) not null,
	rev double precision,
	constraint mid_poseidon_day_ad_revenue_pkey
		primary key (app_name, country, date, vendor, placement_name)
)
sortkey(country);

alter table public.mid_poseidon_day_ad_revenue owner to gv_root;

grant select on public.mid_poseidon_day_ad_revenue to gv_ro;

grant select on public.mid_poseidon_day_ad_revenue to gv_online_ro;

grant select on public.mid_poseidon_day_ad_revenue to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_poseidon_day_ad_revenue to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.mid_poseidon_day_ad_revenue to gv_offline_rw;

grant select on public.mid_poseidon_day_ad_revenue to metabase;

grant select on public.mid_poseidon_day_ad_revenue to gv_developer;

