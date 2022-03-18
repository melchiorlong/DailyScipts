create table public.temp_psd_applovin
(
	ilrd_country varchar(32),
	ad_sum double precision
);

alter table public.temp_psd_applovin owner to awsuser;

grant select on public.temp_psd_applovin to gv_ro;

grant select on public.temp_psd_applovin to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.temp_psd_applovin to gv_online_rw;

grant select on public.temp_psd_applovin to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.temp_psd_applovin to gv_offline_rw;

grant select on public.temp_psd_applovin to gv_alert;

grant select on public.temp_psd_applovin to dev_user;

