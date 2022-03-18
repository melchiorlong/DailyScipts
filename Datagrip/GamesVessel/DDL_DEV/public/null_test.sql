create table public.null_test
(
	muid varchar(20),
	data integer encode az64
);

alter table public.null_test owner to gv_ro;

