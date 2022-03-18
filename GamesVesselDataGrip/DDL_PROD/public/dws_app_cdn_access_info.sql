create table public.dws_app_cdn_access_info
(
	utc_date date,
	location varchar(8),
	host varchar(32),
	http_method varchar(8),
	protocol varchar(5),
	req_cnt bigint encode az64,
	dl_bytes bigint encode az64
)
sortkey(utc_date, location, host, http_method, protocol);

alter table public.dws_app_cdn_access_info owner to gv_root;

grant select on public.dws_app_cdn_access_info to gv_ro;

grant select on public.dws_app_cdn_access_info to gv_online_ro;

grant select on public.dws_app_cdn_access_info to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.dws_app_cdn_access_info to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.dws_app_cdn_access_info to gv_offline_rw;

grant select on public.dws_app_cdn_access_info to metabase;

grant select on public.dws_app_cdn_access_info to gv_developer;

