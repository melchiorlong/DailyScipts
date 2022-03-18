create table public.mid_ilrd_campaign_roi_dnu_and_cost
(
	campaign_id varchar(64) not null,
	bj_date timestamp not null,
	kch_dnu integer encode az64,
	cost double precision,
	constraint mid_ilrd_campaign_roi_dnu_and_cost_pkey
		primary key (campaign_id, bj_date)
)
sortkey(campaign_id, bj_date);

alter table public.mid_ilrd_campaign_roi_dnu_and_cost owner to gv_root;

grant select on public.mid_ilrd_campaign_roi_dnu_and_cost to gv_ro;

grant select on public.mid_ilrd_campaign_roi_dnu_and_cost to gv_online_ro;

grant select on public.mid_ilrd_campaign_roi_dnu_and_cost to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_campaign_roi_dnu_and_cost to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_campaign_roi_dnu_and_cost to gv_offline_rw;

grant select on public.mid_ilrd_campaign_roi_dnu_and_cost to metabase;

grant select on public.mid_ilrd_campaign_roi_dnu_and_cost to gv_developer;

