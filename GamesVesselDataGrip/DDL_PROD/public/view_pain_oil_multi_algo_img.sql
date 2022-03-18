create view view_pain_oil_multi_algo_img as
select *
from public.pain_oil_multi_algo_img
where transmission_version = (select max(transmission_version) from public.pain_oil_multi_algo_img)
with no schema binding;

alter table public.view_pain_oil_multi_algo_img owner to gv_root;

grant select on public.view_pain_oil_multi_algo_img to gv_ro;

grant select on public.view_pain_oil_multi_algo_img to gv_online_ro;

grant select on public.view_pain_oil_multi_algo_img to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.view_pain_oil_multi_algo_img to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.view_pain_oil_multi_algo_img to gv_offline_rw;

grant select on public.view_pain_oil_multi_algo_img to metabase;

grant select on public.view_pain_oil_multi_algo_img to gv_developer;

