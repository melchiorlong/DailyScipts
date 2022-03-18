create table public.mid_ilrd_quality_check_poseidon
(
	bj_date date encode az64,
	app_name varchar(16),
	country varchar(8),
	ad_format varchar(64),
	network varchar(64),
	rev double precision,
	impr bigint encode az64
);

alter table public.mid_ilrd_quality_check_poseidon owner to awsuser;

grant select on public.mid_ilrd_quality_check_poseidon to gv_ro;

grant select on public.mid_ilrd_quality_check_poseidon to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_quality_check_poseidon to gv_online_rw;

grant select on public.mid_ilrd_quality_check_poseidon to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_quality_check_poseidon to gv_offline_rw;

grant select on public.mid_ilrd_quality_check_poseidon to gv_alert;

grant select on public.mid_ilrd_quality_check_poseidon to dev_user;

