create table public.mid_ilrd_quality_check_dau
(
	bj_date date encode az64,
	app_name varchar(16),
	country varchar(8),
	total_dau bigint encode az64,
	ilrd_dau bigint encode az64,
	ads_dau bigint encode az64
);

alter table public.mid_ilrd_quality_check_dau owner to awsuser;

grant select on public.mid_ilrd_quality_check_dau to gv_ro;

grant select on public.mid_ilrd_quality_check_dau to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_quality_check_dau to gv_online_rw;

grant select on public.mid_ilrd_quality_check_dau to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_quality_check_dau to gv_offline_rw;

grant select on public.mid_ilrd_quality_check_dau to gv_alert;

grant select on public.mid_ilrd_quality_check_dau to dev_user;

