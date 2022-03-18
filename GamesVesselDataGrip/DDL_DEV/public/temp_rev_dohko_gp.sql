create table public.temp_rev_dohko_gp
(
	muid varchar(64),
	ins_date date encode az64,
	day_diff integer encode az64,
	ads_rev double precision,
	iap_rev double precision,
	rev double precision
);

alter table public.temp_rev_dohko_gp owner to awsuser;

grant select on public.temp_rev_dohko_gp to gv_ro;

grant select on public.temp_rev_dohko_gp to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.temp_rev_dohko_gp to gv_online_rw;

grant select on public.temp_rev_dohko_gp to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.temp_rev_dohko_gp to gv_offline_rw;

grant select on public.temp_rev_dohko_gp to gv_alert;

grant select on public.temp_rev_dohko_gp to dev_user;

