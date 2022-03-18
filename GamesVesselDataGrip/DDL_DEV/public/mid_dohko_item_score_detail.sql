create table public.mid_dohko_item_score_detail
(
	stat_version bigint encode az64,
	item_id varchar(64),
	algo_version varchar(16),
	country varchar(8),
	begin_recommend_count integer encode az64,
	show_recommend_count integer encode az64,
	begin_count integer encode az64,
	complete_count integer encode az64,
	another_play_count integer encode az64,
	click_rate double precision,
	complete_rate double precision,
	anp_rate double precision,
	duration_sum bigint encode az64,
	duration_count integer encode az64,
	difc double precision,
	score_4_factors double precision,
	score_3_factors double precision,
	score_low_difc double precision,
	thumbnail_url varchar(256),
	online_time timestamp encode az64,
	avg_duration double precision,
	technology_level varchar(4)
);

alter table public.mid_dohko_item_score_detail owner to awsuser;

grant select on public.mid_dohko_item_score_detail to gv_ro;

grant select on public.mid_dohko_item_score_detail to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.mid_dohko_item_score_detail to gv_online_rw;

grant select on public.mid_dohko_item_score_detail to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_dohko_item_score_detail to gv_offline_rw;

grant select on public.mid_dohko_item_score_detail to gv_alert;

grant select on public.mid_dohko_item_score_detail to dev_user;

