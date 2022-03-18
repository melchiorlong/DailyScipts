create table public.poseidon_unittest_muid_ip_mapper
(
	muid varchar(64),
	ip varchar(64)
);

alter table public.poseidon_unittest_muid_ip_mapper owner to awsuser;

grant select on public.poseidon_unittest_muid_ip_mapper to gv_ro;

grant select on public.poseidon_unittest_muid_ip_mapper to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_unittest_muid_ip_mapper to gv_online_rw;

grant select on public.poseidon_unittest_muid_ip_mapper to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_unittest_muid_ip_mapper to gv_offline_rw;

grant select on public.poseidon_unittest_muid_ip_mapper to gv_alert;

grant select on public.poseidon_unittest_muid_ip_mapper to dev_user;

