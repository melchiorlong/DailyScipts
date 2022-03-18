create table public.kch_aiolos_ip_install_info
(
	adid varchar(64),
	app_version integer encode az64,
	media_source varchar(64),
	country_code varchar(8),
	date_occurred timestamp encode az64,
	date_received timestamp,
	device_model varchar(256),
	device_os_version varchar(64),
	idfa varchar(64),
	idfv varchar(64),
	install_id varchar(16),
	ip_address varchar(64),
	kochava_device_id varchar(64),
	network_name varchar(32),
	campaign_id varchar(64),
	fb_account_id varchar(32),
	fb_adset_name varchar(256),
	creative_name varchar(2048),
	source_id varchar(32),
	unity_gamer_id varchar(256),
	applovin_click_id varchar(128)
)
sortkey(date_received);

alter table public.kch_aiolos_ip_install_info owner to awsuser;

grant select on public.kch_aiolos_ip_install_info to gv_ro;

grant select on public.kch_aiolos_ip_install_info to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.kch_aiolos_ip_install_info to gv_online_rw;

grant select on public.kch_aiolos_ip_install_info to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.kch_aiolos_ip_install_info to gv_offline_rw;

grant select on public.kch_aiolos_ip_install_info to gv_alert;

grant select on public.kch_aiolos_ip_install_info to dev_user;

