create table public.mid_dh_ua_data
(
	date timestamp,
	media_source varchar(32),
	campaign_id varchar(128),
	country varchar(32),
	ad_account_id varchar(128),
	campaign_name varchar(128),
	app_name varchar(32),
	optimizer varchar(64),
	team varchar(32),
	impressions bigint encode az64,
	installs bigint encode az64,
	clicks bigint encode az64,
	spend double precision
)
sortkey(date, media_source, campaign_id, country);

alter table public.mid_dh_ua_data owner to gv_root;

grant select on public.mid_dh_ua_data to gv_ro;

grant select on public.mid_dh_ua_data to gv_online_ro;

grant select on public.mid_dh_ua_data to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_dh_ua_data to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.mid_dh_ua_data to gv_offline_rw;

grant select on public.mid_dh_ua_data to metabase;

grant select on public.mid_dh_ua_data to gv_developer;

