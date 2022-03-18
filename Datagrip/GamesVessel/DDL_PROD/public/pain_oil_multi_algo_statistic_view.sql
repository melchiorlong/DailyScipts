create view pain_oil_multi_algo_statistic_view as
select *
from public.pain_oil_multi_algo_statistic
where version_code = (select max(version_code) from public.pain_oil_multi_algo_statistic)
with no schema binding;

alter table public.pain_oil_multi_algo_statistic_view owner to gv_root;

grant select on public.pain_oil_multi_algo_statistic_view to gv_ro;

grant select on public.pain_oil_multi_algo_statistic_view to gv_online_ro;

grant select on public.pain_oil_multi_algo_statistic_view to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.pain_oil_multi_algo_statistic_view to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.pain_oil_multi_algo_statistic_view to gv_offline_rw;

grant select on public.pain_oil_multi_algo_statistic_view to metabase;

grant select on public.pain_oil_multi_algo_statistic_view to gv_developer;

