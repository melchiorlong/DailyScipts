create table public.puzl_img_table
(
	id varchar(32),
	file_name varchar(128),
	img_s3_key varchar(128),
	online_time timestamp encode az64
);

alter table public.puzl_img_table owner to gv_root;

grant select on public.puzl_img_table to gv_ro;

grant select on public.puzl_img_table to gv_online_ro;

grant select on public.puzl_img_table to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.puzl_img_table to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.puzl_img_table to gv_offline_rw;

grant select on public.puzl_img_table to metabase;

grant delete, insert, select, update on public.puzl_img_table to gv_developer;

