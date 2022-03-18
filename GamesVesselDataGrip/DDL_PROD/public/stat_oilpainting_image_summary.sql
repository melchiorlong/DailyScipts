create table public.stat_oilpainting_image_summary
(
	action_date varchar(10),
	app_package_name varchar(256),
	app_version_code integer encode az64,
	item_id varchar(256),
	country varchar(256),
	begin_count bigint encode az64,
	complete_count bigint encode az64,
	unknown_count bigint encode az64,
	replay_count bigint encode az64,
	another_play_count bigint encode az64,
	hint_count bigint encode az64,
	show_count bigint encode az64,
	show_recommend_count bigint encode az64,
	begin_recommend_count bigint encode az64,
	duration_sum bigint encode az64,
	duration_count bigint encode az64,
	algo_version varchar(256) default 'default'::character varying
);

alter table public.stat_oilpainting_image_summary owner to gv_root;

grant select on public.stat_oilpainting_image_summary to gv_ro;

grant select on public.stat_oilpainting_image_summary to gv_online_ro;

grant select on public.stat_oilpainting_image_summary to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.stat_oilpainting_image_summary to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.stat_oilpainting_image_summary to gv_offline_rw;

grant select on public.stat_oilpainting_image_summary to metabase;

grant select on public.stat_oilpainting_image_summary to gv_developer;

grant select on public.stat_oilpainting_image_summary to group ad_hoc;

