create table public.pain_oil_multi_algo_statistic
(
	version_code bigint not null encode az64,
	item_id varchar(64) not null,
	algo_version varchar(32) not null,
	begin_count integer not null encode az64,
	complete_count integer not null encode az64,
	another_play_count integer not null encode az64,
	show_recommend_count integer not null encode az64,
	begin_recommend_count integer not null encode az64,
	duration_sum integer not null encode az64,
	duration_count integer not null encode az64,
	duration double precision,
	click_rate double precision,
	complete_rate double precision,
	another_play_rate double precision,
	difc double precision,
	score_4_params double precision,
	score_3_params double precision,
	score_low_difc_weight double precision,
	constraint pain_oil_multi_algo_statistic_pkey
		primary key (version_code, item_id, algo_version)
);

alter table public.pain_oil_multi_algo_statistic owner to gv_root;

grant select on public.pain_oil_multi_algo_statistic to gv_ro;

grant select on public.pain_oil_multi_algo_statistic to gv_online_ro;

grant select on public.pain_oil_multi_algo_statistic to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.pain_oil_multi_algo_statistic to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.pain_oil_multi_algo_statistic to gv_offline_rw;

grant select on public.pain_oil_multi_algo_statistic to metabase;

grant select on public.pain_oil_multi_algo_statistic to gv_developer;

grant select on public.pain_oil_multi_algo_statistic to group ad_hoc;

