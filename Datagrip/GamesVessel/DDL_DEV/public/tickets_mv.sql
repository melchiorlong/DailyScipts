create view public.tickets_mv(media_source) as
	CREATE MATERIALIZED VIEW tickets_mv AS
SELECT media_source
from stat_kch_install_retention_count
where country = 'JP'
  and app_name = 'dohko_ip'
--  and to_timestamp(bj_date,'YYYY-MM-DD')>='2021-04-01' and to_timestamp(bj_date,'YYYY-MM-DD')<= '2021-05-06';

alter table public.tickets_mv owner to gv_ro;

