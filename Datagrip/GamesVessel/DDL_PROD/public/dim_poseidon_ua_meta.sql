create table public.dim_poseidon_ua_meta
(
	media_source varchar(32),
	campaign_id varchar(128),
	ad_account_id varchar(128),
	campaign_name varchar(128),
	app_name varchar(32),
	optimizer varchar(64),
	team varchar(32),
	optimizer_id varchar(128)
)
sortkey(media_source, campaign_id);

alter table public.dim_poseidon_ua_meta owner to gv_root;

grant select on public.dim_poseidon_ua_meta to gv_ro;

grant select on public.dim_poseidon_ua_meta to gv_online_ro;

grant select on public.dim_poseidon_ua_meta to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.dim_poseidon_ua_meta to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.dim_poseidon_ua_meta to gv_offline_rw;

grant select on public.dim_poseidon_ua_meta to metabase;

grant select on public.dim_poseidon_ua_meta to gv_developer;

