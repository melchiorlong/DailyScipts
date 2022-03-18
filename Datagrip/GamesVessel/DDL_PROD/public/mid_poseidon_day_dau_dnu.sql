create table public.mid_poseidon_day_dau_dnu
(
	date timestamp encode az64,
	app_name varchar(16),
	country varchar(8),
	flurry_dau integer encode az64,
	flurry_dnu integer encode az64,
	kch_dau integer encode az64,
	kch_dnu integer encode az64
);

alter table public.mid_poseidon_day_dau_dnu owner to gv_root;

grant select on public.mid_poseidon_day_dau_dnu to gv_ro;

grant select on public.mid_poseidon_day_dau_dnu to gv_online_ro;

grant select on public.mid_poseidon_day_dau_dnu to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_poseidon_day_dau_dnu to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.mid_poseidon_day_dau_dnu to gv_offline_rw;

grant select on public.mid_poseidon_day_dau_dnu to metabase;

grant select on public.mid_poseidon_day_dau_dnu to gv_developer;

