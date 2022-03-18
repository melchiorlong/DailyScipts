create table public.dwd_poseidon_coin_analysis_balance
(
	app_name varchar(9),
	muid varchar(64),
	country_code varchar(8),
	install_date date encode az64,
	day_dimension integer encode az64,
	balance_fillwith_last_value integer encode az64,
	balance_fill_zero integer encode az64
);

alter table public.dwd_poseidon_coin_analysis_balance owner to awsuser;

grant select on public.dwd_poseidon_coin_analysis_balance to gv_ro;

grant select on public.dwd_poseidon_coin_analysis_balance to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.dwd_poseidon_coin_analysis_balance to gv_online_rw;

grant select on public.dwd_poseidon_coin_analysis_balance to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.dwd_poseidon_coin_analysis_balance to gv_offline_rw;

grant select on public.dwd_poseidon_coin_analysis_balance to gv_alert;

grant select on public.dwd_poseidon_coin_analysis_balance to dev_user;

