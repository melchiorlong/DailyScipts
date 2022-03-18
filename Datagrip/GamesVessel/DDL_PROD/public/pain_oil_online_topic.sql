create table public.pain_oil_online_topic
(
	id integer not null encode az64,
	topic_id varchar(16) not null,
	price integer not null encode az64,
	img_count integer not null encode az64,
	img_key varchar(256) not null,
	country_filter varchar(256) not null,
	thumbs varchar(256) not null,
	lang_pack varchar(256) not null,
	close_time timestamp encode az64,
	create_time timestamp encode az64,
	update_time timestamp encode az64
);

alter table public.pain_oil_online_topic owner to gv_root;

grant select on public.pain_oil_online_topic to gv_ro;

grant select on public.pain_oil_online_topic to gv_online_ro;

grant select on public.pain_oil_online_topic to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.pain_oil_online_topic to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.pain_oil_online_topic to gv_offline_rw;

grant select on public.pain_oil_online_topic to metabase;

grant delete, insert, select, update on public.pain_oil_online_topic to gv_developer;

