create view pain_oil_topic_view as
select *
from public.pain_oil_topic
where transmission_version = (select max(transmission_version) from public.pain_oil_topic)
with no schema binding;

alter table public.pain_oil_topic_view owner to gv_root;

grant select on public.pain_oil_topic_view to gv_ro;

grant select on public.pain_oil_topic_view to gv_online_ro;

grant select on public.pain_oil_topic_view to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.pain_oil_topic_view to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.pain_oil_topic_view to gv_offline_rw;

grant select on public.pain_oil_topic_view to metabase;

grant select on public.pain_oil_topic_view to gv_developer;

