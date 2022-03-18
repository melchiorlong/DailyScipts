create view public.tick(a1, a2, a3) as
	CREATE MATERIALIZED VIEW tick AUTO REFRESH YES AS

SELECT *
from test
where a2 = 'we';

alter table public.tick owner to gv_ro;

