create table public.muid_dimension
(
	muid varchar(64),
	device_id varchar(64),
	app_name varchar(16),
	media_source varchar(64),
	kch_country varchar(32),
	kch_id varchar(64),
	app_install_version smallint encode az64,
	install_bj_datetime timestamp encode az64,
	country varchar(7)
)
sortkey(muid);

comment on column public.muid_dimension.app_install_version is '应用安装时的版本号';

comment on column public.muid_dimension.install_bj_datetime is '用户安装的北京时间';

comment on column public.muid_dimension.country is '两位大写ISO国家字母码的格式';

alter table public.muid_dimension owner to gv_root;

grant select on public.muid_dimension to gv_ro;

grant select on public.muid_dimension to gv_online_ro;

grant select on public.muid_dimension to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.muid_dimension to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.muid_dimension to gv_offline_rw;

grant select on public.muid_dimension to metabase;

grant select on public.muid_dimension to gv_developer;

