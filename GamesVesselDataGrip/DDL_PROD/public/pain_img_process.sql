create table public.pain_img_process
(
	id varchar(50) not null distkey
		constraint pain_img_process_pkey
			primary key,
	name varchar(50) not null,
	category_id integer encode az64,
	status integer not null encode az64,
	error_info varchar(65535),
	origin_file_path varchar(512) not null,
	white_file_path varchar(512),
	thumb_path varchar(512),
	color_count integer encode az64,
	publish_time bigint encode az64,
	scheduled_time bigint encode az64,
	technology_level varchar(64),
	color_list_path varchar(512),
	zip_path varchar(512),
	lattice_count integer encode az64,
	test_record varchar(65535),
	tag_ids varchar(512),
	review_record varchar(65535),
	online_record varchar(65535),
	online_time timestamp encode az64,
	create_time timestamp not null encode az64,
	update_time timestamp not null encode az64,
	transmission_version bigint encode az64,
	region_lock_flag varchar(1024),
	tag_ids_v2 varchar(512),
	recommend_abandon integer encode az64
);

alter table public.pain_img_process owner to gv_root;

grant select on public.pain_img_process to gv_ro;

grant select on public.pain_img_process to gv_online_ro;

grant select on public.pain_img_process to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.pain_img_process to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.pain_img_process to gv_offline_rw;

grant select on public.pain_img_process to metabase;

grant select on public.pain_img_process to gv_developer;

grant select on public.pain_img_process to group ad_hoc;

