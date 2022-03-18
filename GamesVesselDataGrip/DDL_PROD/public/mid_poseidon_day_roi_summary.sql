create table public.mid_poseidon_day_roi_summary
(
	app_name varchar(16) not null,
	country varchar(64) not null,
	date timestamp not null,
	rev double precision,
	spend double precision,
	iap_rev double precision,
	ads_rev double precision,
	constraint mid_poseidon_day_roi_summary_pkey
		primary key (app_name, country, date)
)
sortkey(app_name, country, date);

alter table public.mid_poseidon_day_roi_summary owner to gv_root;

grant select on public.mid_poseidon_day_roi_summary to gv_ro;

grant select on public.mid_poseidon_day_roi_summary to gv_online_ro;

grant select on public.mid_poseidon_day_roi_summary to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_poseidon_day_roi_summary to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.mid_poseidon_day_roi_summary to gv_offline_rw;

grant select on public.mid_poseidon_day_roi_summary to metabase;

grant select on public.mid_poseidon_day_roi_summary to gv_developer;

