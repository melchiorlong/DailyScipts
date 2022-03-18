create table public.mid_ilrd_campaign_roi_total_rev
(
	campaign_id varchar(64) not null,
	bj_date timestamp not null,
	day0_ads_rev double precision,
	day0_iap_rev double precision,
	day1_ads_rev double precision,
	day1_iap_rev double precision,
	day3_ads_rev double precision,
	day3_iap_rev double precision,
	day7_ads_rev double precision,
	day7_iap_rev double precision,
	day14_ads_rev double precision,
	day14_iap_rev double precision,
	day30_ads_rev double precision,
	day30_iap_rev double precision,
	day0_ads_rev_include_fb varchar(8),
	day1_ads_rev_include_fb varchar(8),
	day3_ads_rev_include_fb varchar(8),
	day7_ads_rev_include_fb varchar(8),
	day14_ads_rev_include_fb varchar(8),
	day30_ads_rev_include_fb varchar(8),
	country varchar(8),
	day2_ads_rev double precision,
	day2_iap_rev double precision,
	day2_ads_rev_include_fb varchar(8),
	constraint mid_ilrd_campaign_roi_total_rev_pkey
		primary key (campaign_id, bj_date)
)
sortkey(campaign_id, bj_date);

alter table public.mid_ilrd_campaign_roi_total_rev owner to gv_root;

grant select on public.mid_ilrd_campaign_roi_total_rev to gv_ro;

grant select on public.mid_ilrd_campaign_roi_total_rev to gv_online_ro;

grant select on public.mid_ilrd_campaign_roi_total_rev to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_campaign_roi_total_rev to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_campaign_roi_total_rev to gv_offline_rw;

grant select on public.mid_ilrd_campaign_roi_total_rev to metabase;

grant select on public.mid_ilrd_campaign_roi_total_rev to gv_developer;

