create table public.mid_ilrd_campaign_roi_dnu_and_cost
(
	campaign_id varchar(64) not null,
	bj_date timestamp not null encode az64,
	kch_dnu integer encode az64,
	cost double precision
);

alter table public.mid_ilrd_campaign_roi_dnu_and_cost owner to awsuser;

grant select on public.mid_ilrd_campaign_roi_dnu_and_cost to gv_ro;

grant select on public.mid_ilrd_campaign_roi_dnu_and_cost to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_campaign_roi_dnu_and_cost to gv_online_rw;

grant select on public.mid_ilrd_campaign_roi_dnu_and_cost to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_campaign_roi_dnu_and_cost to gv_offline_rw;

grant select on public.mid_ilrd_campaign_roi_dnu_and_cost to gv_alert;

grant select on public.mid_ilrd_campaign_roi_dnu_and_cost to dev_user;

