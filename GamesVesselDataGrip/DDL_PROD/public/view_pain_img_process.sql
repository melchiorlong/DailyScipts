create view view_pain_img_process as
select *
from public.pain_img_process
where transmission_version = (select max(transmission_version) from public.pain_img_process)
with no schema binding;

comment on view public.view_pain_img_process is 'painting图片';

alter table public.view_pain_img_process owner to gv_root;

grant select on public.view_pain_img_process to gv_ro;

grant select on public.view_pain_img_process to gv_online_ro;

grant select on public.view_pain_img_process to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.view_pain_img_process to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.view_pain_img_process to gv_offline_rw;

grant select on public.view_pain_img_process to metabase;

grant select on public.view_pain_img_process to gv_developer;

