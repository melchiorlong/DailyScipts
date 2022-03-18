create table public.fact_poseidon_ua_metric
(
	date timestamp encode az64,
	media_source varchar(32),
	campaign_id varchar(128),
	country varchar(32),
	impressions bigint encode az64,
	installs bigint encode az64,
	clicks bigint encode az64,
	spend double precision
);

alter table public.fact_poseidon_ua_metric owner to awsuser;

grant select on public.fact_poseidon_ua_metric to gv_ro;

grant select on public.fact_poseidon_ua_metric to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.fact_poseidon_ua_metric to gv_online_rw;

grant select on public.fact_poseidon_ua_metric to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.fact_poseidon_ua_metric to gv_offline_rw;

grant select on public.fact_poseidon_ua_metric to gv_alert;

grant select on public.fact_poseidon_ua_metric to dev_user;

