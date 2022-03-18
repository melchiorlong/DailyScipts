create table public.mid_poseidon_day_ad_revenue_by_placement
(
	app_name varchar(16) not null,
	country varchar(64) not null,
	date timestamp not null encode az64,
	placement_name varchar(64),
	rev double precision
);

alter table public.mid_poseidon_day_ad_revenue_by_placement owner to awsuser;

grant select on public.mid_poseidon_day_ad_revenue_by_placement to gv_ro;

grant select on public.mid_poseidon_day_ad_revenue_by_placement to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.mid_poseidon_day_ad_revenue_by_placement to gv_online_rw;

grant select on public.mid_poseidon_day_ad_revenue_by_placement to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_poseidon_day_ad_revenue_by_placement to gv_offline_rw;

grant select on public.mid_poseidon_day_ad_revenue_by_placement to gv_alert;

grant select on public.mid_poseidon_day_ad_revenue_by_placement to dev_user;

