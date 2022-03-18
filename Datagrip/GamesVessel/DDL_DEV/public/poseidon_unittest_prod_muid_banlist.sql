create table public.poseidon_unittest_prod_muid_banlist
(
	ban_date date encode az64,
	muid varchar(64),
	reason smallint encode az64,
	duration integer encode az64
);

alter table public.poseidon_unittest_prod_muid_banlist owner to awsuser;

grant select on public.poseidon_unittest_prod_muid_banlist to gv_ro;

grant select on public.poseidon_unittest_prod_muid_banlist to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_unittest_prod_muid_banlist to gv_online_rw;

grant select on public.poseidon_unittest_prod_muid_banlist to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.poseidon_unittest_prod_muid_banlist to gv_offline_rw;

grant select on public.poseidon_unittest_prod_muid_banlist to gv_alert;

grant select on public.poseidon_unittest_prod_muid_banlist to dev_user;

