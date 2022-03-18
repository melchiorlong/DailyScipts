create table public.puzl_topic_info
(
	id varchar(32),
	name varchar(4096),
	open_date timestamp encode az64,
	thumb_s3_keys varchar(4096)
);

alter table public.puzl_topic_info owner to gv_root;

grant select on public.puzl_topic_info to gv_ro;

grant select on public.puzl_topic_info to gv_online_ro;

grant select on public.puzl_topic_info to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.puzl_topic_info to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.puzl_topic_info to gv_offline_rw;

grant select on public.puzl_topic_info to metabase;

grant delete, insert, select, update on public.puzl_topic_info to gv_developer;

