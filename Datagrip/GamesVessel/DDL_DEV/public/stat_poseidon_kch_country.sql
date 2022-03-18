create table public.stat_poseidon_kch_country
(
	country varchar(8)
);

alter table public.stat_poseidon_kch_country owner to awsuser;

grant select on public.stat_poseidon_kch_country to gv_ro;

grant select on public.stat_poseidon_kch_country to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.stat_poseidon_kch_country to gv_online_rw;

grant select on public.stat_poseidon_kch_country to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.stat_poseidon_kch_country to gv_offline_rw;

grant select on public.stat_poseidon_kch_country to gv_alert;

grant select on public.stat_poseidon_kch_country to dev_user;

