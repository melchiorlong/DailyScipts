create table public.mid_ilrd_dh_fb_cpm
(
	date timestamp not null,
	app_name varchar(64) not null,
	country varchar(64) not null,
	fb_cpm double precision,
	total_rev double precision,
	total_impr integer encode az64,
	constraint mid_ilrd_dh_fb_cpm_pkey
		primary key (date, app_name, country)
)
sortkey(date);

alter table public.mid_ilrd_dh_fb_cpm owner to gv_root;

grant select on public.mid_ilrd_dh_fb_cpm to gv_ro;

grant select on public.mid_ilrd_dh_fb_cpm to gv_online_ro;

grant select on public.mid_ilrd_dh_fb_cpm to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_dh_fb_cpm to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.mid_ilrd_dh_fb_cpm to gv_offline_rw;

grant select on public.mid_ilrd_dh_fb_cpm to metabase;

grant select on public.mid_ilrd_dh_fb_cpm to gv_developer;

