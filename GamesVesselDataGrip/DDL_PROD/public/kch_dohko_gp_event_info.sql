create table public.kch_dohko_gp_event_info
(
	date_occurred timestamp encode zstd,
	date_received timestamp,
	event_name varchar(64) encode zstd,
	install_id varchar(16) encode zstd distkey,
	kochava_device_id varchar(64) encode zstd
)
sortkey(date_received);

alter table public.kch_dohko_gp_event_info owner to gv_root;

grant select on public.kch_dohko_gp_event_info to gv_ro;

grant select on public.kch_dohko_gp_event_info to gv_online_ro;

grant select on public.kch_dohko_gp_event_info to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.kch_dohko_gp_event_info to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.kch_dohko_gp_event_info to gv_offline_rw;

grant select on public.kch_dohko_gp_event_info to metabase;

grant select on public.kch_dohko_gp_event_info to gv_developer;

