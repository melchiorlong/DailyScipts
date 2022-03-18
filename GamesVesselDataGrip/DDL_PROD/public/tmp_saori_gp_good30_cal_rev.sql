create table public.tmp_saori_gp_good30_cal_rev
(
	muid varchar(64),
	country varchar(8),
	cal_day0_rev double precision,
	cal_day1_rev double precision,
	cal_day2_rev double precision,
	cal_day3_rev double precision,
	cal_day4_rev double precision,
	cal_day5_rev double precision,
	cal_day6_rev double precision,
	cal_day7_rev double precision
);

alter table public.tmp_saori_gp_good30_cal_rev owner to gv_root;

grant select on public.tmp_saori_gp_good30_cal_rev to gv_ro;

grant select on public.tmp_saori_gp_good30_cal_rev to gv_online_ro;

grant select on public.tmp_saori_gp_good30_cal_rev to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.tmp_saori_gp_good30_cal_rev to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.tmp_saori_gp_good30_cal_rev to gv_offline_rw;

grant select on public.tmp_saori_gp_good30_cal_rev to metabase;

grant select on public.tmp_saori_gp_good30_cal_rev to gv_developer;

