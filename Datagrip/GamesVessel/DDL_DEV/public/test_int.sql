create table public.test_int
(
	a integer encode az64
);

alter table public.test_int owner to gv_offline_rw;

