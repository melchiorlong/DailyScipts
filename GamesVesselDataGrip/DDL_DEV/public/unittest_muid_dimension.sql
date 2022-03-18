create table public.unittest_muid_dimension
(
	muid varchar(64),
	device_id varchar(64)
);

alter table public.unittest_muid_dimension owner to awsuser;

grant select on public.unittest_muid_dimension to gv_ro;

grant select on public.unittest_muid_dimension to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.unittest_muid_dimension to gv_online_rw;

grant select on public.unittest_muid_dimension to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.unittest_muid_dimension to gv_offline_rw;

grant select on public.unittest_muid_dimension to gv_alert;

grant select on public.unittest_muid_dimension to dev_user;

