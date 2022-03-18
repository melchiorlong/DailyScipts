create table public.kch_dohko_ip_event_info
(
	date_occurred timestamp encode az64,
	date_received timestamp encode az64,
	event_name varchar(64),
	install_id varchar(16),
	kochava_device_id varchar(64)
);

alter table public.kch_dohko_ip_event_info owner to awsuser;

grant select on public.kch_dohko_ip_event_info to gv_ro;

grant select on public.kch_dohko_ip_event_info to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.kch_dohko_ip_event_info to gv_online_rw;

grant select on public.kch_dohko_ip_event_info to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.kch_dohko_ip_event_info to gv_offline_rw;

grant select on public.kch_dohko_ip_event_info to gv_alert;

grant select on public.kch_dohko_ip_event_info to dev_user;

