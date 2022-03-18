create table public.pain_oil_topic
(
	id varchar(256),
	price integer encode az64,
	tag_ids varchar(1024),
	thumbs varchar(1024),
	op_record varchar(1024),
	status integer encode az64,
	country_filter varchar(1024),
	open_time timestamp encode az64,
	close_time timestamp encode az64,
	create_time timestamp encode az64,
	update_time timestamp encode az64,
	transmission_version bigint encode az64
);

alter table public.pain_oil_topic owner to gv_root;

grant select on public.pain_oil_topic to gv_ro;

grant select on public.pain_oil_topic to gv_online_ro;

grant select on public.pain_oil_topic to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.pain_oil_topic to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.pain_oil_topic to gv_offline_rw;

grant select on public.pain_oil_topic to metabase;

grant select on public.pain_oil_topic to gv_developer;

