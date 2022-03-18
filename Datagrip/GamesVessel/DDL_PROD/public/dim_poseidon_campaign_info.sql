create table public.dim_poseidon_campaign_info
(
	campaign_id varchar(64),
	campaign_name varchar(128),
	team varchar(64),
	optimizer varchar(256),
	source varchar(32),
	campaign_app_name varchar(16),
	campaign_media_source varchar(64)
)
sortkey(campaign_id);

alter table public.dim_poseidon_campaign_info owner to gv_root;

grant select on public.dim_poseidon_campaign_info to gv_ro;

grant select on public.dim_poseidon_campaign_info to gv_online_ro;

grant select on public.dim_poseidon_campaign_info to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.dim_poseidon_campaign_info to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.dim_poseidon_campaign_info to gv_offline_rw;

grant select on public.dim_poseidon_campaign_info to metabase;

grant select on public.dim_poseidon_campaign_info to gv_developer;

