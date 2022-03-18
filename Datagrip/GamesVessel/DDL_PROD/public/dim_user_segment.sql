create table public.dim_user_segment
(
	muid varchar(64),
	user_segment varchar(32),
	action_bj_date date encode az64
);

alter table public.dim_user_segment owner to gv_root;

grant select on public.dim_user_segment to gv_ro;

grant select on public.dim_user_segment to dev_user;

grant select on public.dim_user_segment to gv_online_ro;

grant select on public.dim_user_segment to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.dim_user_segment to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.dim_user_segment to gv_offline_rw;

grant select on public.dim_user_segment to gv_alert;

grant select on public.dim_user_segment to metabase;

grant select on public.dim_user_segment to gv_developer;

