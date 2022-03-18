create table public.mid_ilrd_campaign_roi_daily_fbimpr
(
	campaign_id varchar(64),
	country varchar(8),
	install_bj_date timestamp encode az64,
	rev_bj_date timestamp encode az64,
	fb_impr integer encode az64,
	fb_impr_with_organic integer encode az64
);

alter table public.mid_ilrd_campaign_roi_daily_fbimpr owner to awsuser;

grant select on public.mid_ilrd_campaign_roi_daily_fbimpr to gv_ro;

grant select on public.mid_ilrd_campaign_roi_daily_fbimpr to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_campaign_roi_daily_fbimpr to gv_online_rw;

grant select on public.mid_ilrd_campaign_roi_daily_fbimpr to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_campaign_roi_daily_fbimpr to gv_offline_rw;

grant select on public.mid_ilrd_campaign_roi_daily_fbimpr to gv_alert;

grant select on public.mid_ilrd_campaign_roi_daily_fbimpr to dev_user;

