create table public.mid_dh_sales_detail
(
	date timestamp,
	iap_source varchar(64),
	app_id varchar(64),
	app_name varchar(16),
	country varchar(8),
	sku varchar(64),
	rev double precision
)
sortkey(date, iap_source, app_id, app_name, country, sku);

alter table public.mid_dh_sales_detail owner to gv_root;

grant select on public.mid_dh_sales_detail to gv_ro;

grant select on public.mid_dh_sales_detail to gv_online_ro;

grant select on public.mid_dh_sales_detail to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_dh_sales_detail to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.mid_dh_sales_detail to gv_offline_rw;

grant select on public.mid_dh_sales_detail to metabase;

grant select on public.mid_dh_sales_detail to gv_developer;

