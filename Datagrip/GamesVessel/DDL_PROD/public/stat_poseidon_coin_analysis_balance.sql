create table public.stat_poseidon_coin_analysis_balance
(
	app_name varchar(32),
	muid varchar(64),
	country_code varchar(8),
	install_date date encode az64,
	day_dimension integer encode az64,
	balance_fillwith_last_value integer encode az64,
	balance_fill_zero integer encode az64
);

alter table public.stat_poseidon_coin_analysis_balance owner to gv_root;

grant select on public.stat_poseidon_coin_analysis_balance to gv_ro;

grant select on public.stat_poseidon_coin_analysis_balance to gv_online_ro;

grant select on public.stat_poseidon_coin_analysis_balance to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.stat_poseidon_coin_analysis_balance to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.stat_poseidon_coin_analysis_balance to gv_offline_rw;

grant select on public.stat_poseidon_coin_analysis_balance to metabase;

grant select on public.stat_poseidon_coin_analysis_balance to gv_developer;

