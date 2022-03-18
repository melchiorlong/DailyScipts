create table public.stat_poseidon_coin_analysis_revenue_cost_summary
(
	app_name varchar(32),
	country_code varchar(8),
	install_date date encode az64,
	day_dimension integer encode az64,
	coin_change_type integer encode az64,
	coin_change_reason varchar(64),
	coin_diff_summary bigint encode az64
);

alter table public.stat_poseidon_coin_analysis_revenue_cost_summary owner to gv_root;

grant select on public.stat_poseidon_coin_analysis_revenue_cost_summary to gv_ro;

grant select on public.stat_poseidon_coin_analysis_revenue_cost_summary to gv_online_ro;

grant select on public.stat_poseidon_coin_analysis_revenue_cost_summary to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.stat_poseidon_coin_analysis_revenue_cost_summary to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.stat_poseidon_coin_analysis_revenue_cost_summary to gv_offline_rw;

grant select on public.stat_poseidon_coin_analysis_revenue_cost_summary to metabase;

grant select on public.stat_poseidon_coin_analysis_revenue_cost_summary to gv_developer;

