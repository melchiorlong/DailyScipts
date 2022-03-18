create table public.mid_dh_sales_detail
(
	date timestamp encode az64,
	iap_source varchar(64),
	app_id varchar(64),
	app_name varchar(16),
	country varchar(8),
	sku varchar(64),
	rev double precision
);

alter table public.mid_dh_sales_detail owner to awsuser;

grant select on public.mid_dh_sales_detail to gv_ro;

grant select on public.mid_dh_sales_detail to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.mid_dh_sales_detail to gv_online_rw;

grant select on public.mid_dh_sales_detail to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_dh_sales_detail to gv_offline_rw;

grant select on public.mid_dh_sales_detail to gv_alert;

grant select on public.mid_dh_sales_detail to dev_user;

