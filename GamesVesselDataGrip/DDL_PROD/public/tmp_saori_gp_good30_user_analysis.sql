create table public.tmp_saori_gp_good30_user_analysis
(
	muid varchar(64),
	country_code varchar(8),
	bj_date date encode az64
);

alter table public.tmp_saori_gp_good30_user_analysis owner to gv_root;

grant select on public.tmp_saori_gp_good30_user_analysis to gv_ro;

grant select on public.tmp_saori_gp_good30_user_analysis to gv_online_ro;

grant select on public.tmp_saori_gp_good30_user_analysis to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.tmp_saori_gp_good30_user_analysis to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.tmp_saori_gp_good30_user_analysis to gv_offline_rw;

grant select on public.tmp_saori_gp_good30_user_analysis to metabase;

grant select on public.tmp_saori_gp_good30_user_analysis to gv_developer;

