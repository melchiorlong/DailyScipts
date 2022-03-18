create view mid_dohko_item_score_detail_view as
select *
from public.mid_dohko_item_score_detail
where stat_version = (
    select max(stat_version)
    from public.mid_dohko_item_score_detail
)
with no schema binding;

alter table public.mid_dohko_item_score_detail_view owner to gv_root;

grant select on public.mid_dohko_item_score_detail_view to gv_ro;

grant select on public.mid_dohko_item_score_detail_view to gv_online_ro;

grant select on public.mid_dohko_item_score_detail_view to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_dohko_item_score_detail_view to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.mid_dohko_item_score_detail_view to gv_offline_rw;

grant select on public.mid_dohko_item_score_detail_view to metabase;

grant select on public.mid_dohko_item_score_detail_view to gv_developer;

