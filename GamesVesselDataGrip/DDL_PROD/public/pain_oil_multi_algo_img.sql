create table public.pain_oil_multi_algo_img
(
	id varchar(50) not null,
	algo_version varchar(32) not null,
	name varchar(50) not null,
	source_file_path varchar(512),
	source_url varchar(512),
	origin_file_path varchar(512) not null,
	white_file_path varchar(512),
	thumb_path varchar(512),
	color_list_path varchar(512),
	zip_path varchar(512),
	lattice_count integer encode az64,
	tag_ids varchar(512),
	color_count integer encode az64,
	technology_level varchar(64),
	status integer not null encode az64,
	error_info varchar(65535),
	publish_time bigint encode az64,
	scheduled_time bigint encode az64,
	online_time timestamp encode az64,
	review_record varchar(65535),
	online_record varchar(65535),
	create_time timestamp not null encode az64,
	update_time timestamp not null encode az64,
	transmission_version bigint encode az64,
	tag_ids_v2 varchar(512),
	thumb_colored_path varchar(512),
	constraint pain_oil_multi_algo_img_pkey
		primary key (id, algo_version)
);

alter table public.pain_oil_multi_algo_img owner to gv_root;

grant select on public.pain_oil_multi_algo_img to gv_ro;

grant select on public.pain_oil_multi_algo_img to gv_online_ro;

grant select on public.pain_oil_multi_algo_img to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.pain_oil_multi_algo_img to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.pain_oil_multi_algo_img to gv_offline_rw;

grant select on public.pain_oil_multi_algo_img to metabase;

grant select on public.pain_oil_multi_algo_img to gv_developer;

grant select on public.pain_oil_multi_algo_img to group ad_hoc;

