create table public.stat_poseidon_coin_analysis_revenue_cost
(
	app_name varchar(32),
	muid varchar(64),
	country_code varchar(8),
	install_date date encode az64,
	coin_change_type integer encode az64,
	coin_change_reason varchar(64),
	day_dimension integer encode az64,
	coin_diff bigint encode az64
);

alter table public.stat_poseidon_coin_analysis_revenue_cost owner to gv_root;

grant select on public.stat_poseidon_coin_analysis_revenue_cost to gv_ro;

grant select on public.stat_poseidon_coin_analysis_revenue_cost to gv_online_ro;

grant select on public.stat_poseidon_coin_analysis_revenue_cost to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.stat_poseidon_coin_analysis_revenue_cost to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.stat_poseidon_coin_analysis_revenue_cost to gv_offline_rw;

grant select on public.stat_poseidon_coin_analysis_revenue_cost to metabase;

grant select on public.stat_poseidon_coin_analysis_revenue_cost to gv_developer;

