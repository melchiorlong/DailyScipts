create table public.test
(
	a1 varchar(32),
	a2 varchar(32),
	a3 integer encode az64
);

alter table public.test owner to gv_ro;

