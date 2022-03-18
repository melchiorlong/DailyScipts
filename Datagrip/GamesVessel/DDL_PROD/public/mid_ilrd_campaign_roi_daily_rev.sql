create table public.mid_ilrd_campaign_roi_daily_rev
(
	campaign_id varchar(64),
	install_bj_date timestamp encode az64,
	fb_impr integer encode az64,
	iap_rev double precision,
	rev_bj_date timestamp encode az64,
	ads_revenue_exclude_fb double precision,
	country varchar(8)
)
sortkey(rev_bj_date);

alter table public.mid_ilrd_campaign_roi_daily_rev owner to gv_root;

grant select on public.mid_ilrd_campaign_roi_daily_rev to gv_ro;

grant select on public.mid_ilrd_campaign_roi_daily_rev to gv_online_ro;

grant select on public.mid_ilrd_campaign_roi_daily_rev to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_campaign_roi_daily_rev to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_campaign_roi_daily_rev to gv_offline_rw;

grant select on public.mid_ilrd_campaign_roi_daily_rev to metabase;

grant select on public.mid_ilrd_campaign_roi_daily_rev to gv_developer;

