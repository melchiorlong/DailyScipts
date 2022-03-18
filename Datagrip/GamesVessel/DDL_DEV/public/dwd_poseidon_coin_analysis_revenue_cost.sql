create table public.dwd_poseidon_coin_analysis_revenue_cost
(
	app_name varchar(9),
	muid varchar(64),
	country_code varchar(8),
	install_date date encode az64,
	coin_change_type integer encode az64,
	coin_change_reason varchar(64),
	day_dimension integer encode az64,
	coin_diff bigint encode az64
);

alter table public.dwd_poseidon_coin_analysis_revenue_cost owner to awsuser;

grant select on public.dwd_poseidon_coin_analysis_revenue_cost to gv_ro;

grant select on public.dwd_poseidon_coin_analysis_revenue_cost to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.dwd_poseidon_coin_analysis_revenue_cost to gv_online_rw;

grant select on public.dwd_poseidon_coin_analysis_revenue_cost to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.dwd_poseidon_coin_analysis_revenue_cost to gv_offline_rw;

grant select on public.dwd_poseidon_coin_analysis_revenue_cost to gv_alert;

grant select on public.dwd_poseidon_coin_analysis_revenue_cost to dev_user;

