create table public.dws_poseidon_coin_analysis_revenue_cost
(
	app_name varchar(9),
	country_code varchar(8),
	install_date date,
	day_dimension integer,
	coin_change_type integer encode az64,
	coin_change_reason varchar(64),
	coin_diff_summary bigint encode az64
)
sortkey(app_name, country_code, install_date, day_dimension);

alter table public.dws_poseidon_coin_analysis_revenue_cost owner to awsuser;

grant select on public.dws_poseidon_coin_analysis_revenue_cost to gv_ro;

grant select on public.dws_poseidon_coin_analysis_revenue_cost to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.dws_poseidon_coin_analysis_revenue_cost to gv_online_rw;

grant select on public.dws_poseidon_coin_analysis_revenue_cost to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.dws_poseidon_coin_analysis_revenue_cost to gv_offline_rw;

grant select on public.dws_poseidon_coin_analysis_revenue_cost to gv_alert;

grant select on public.dws_poseidon_coin_analysis_revenue_cost to dev_user;

