create view public.mid_dohko_item_score_detail_view(stat_version, item_id, algo_version, country, begin_recommend_count, show_recommend_count, begin_count, complete_count, another_play_count, click_rate, complete_rate, anp_rate, duration_sum, duration_count, difc, score_4_factors, score_3_factors, score_low_difc, thumbnail_url, online_time, avg_duration, technology_level) as
	SELECT mid_dohko_item_score_detail.stat_version,
       mid_dohko_item_score_detail.item_id,
       mid_dohko_item_score_detail.algo_version,
       mid_dohko_item_score_detail.country,
       mid_dohko_item_score_detail.begin_recommend_count,
       mid_dohko_item_score_detail.show_recommend_count,
       mid_dohko_item_score_detail.begin_count,
       mid_dohko_item_score_detail.complete_count,
       mid_dohko_item_score_detail.another_play_count,
       mid_dohko_item_score_detail.click_rate,
       mid_dohko_item_score_detail.complete_rate,
       mid_dohko_item_score_detail.anp_rate,
       mid_dohko_item_score_detail.duration_sum,
       mid_dohko_item_score_detail.duration_count,
       mid_dohko_item_score_detail.difc,
       mid_dohko_item_score_detail.score_4_factors,
       mid_dohko_item_score_detail.score_3_factors,
       mid_dohko_item_score_detail.score_low_difc,
       mid_dohko_item_score_detail.thumbnail_url,
       mid_dohko_item_score_detail.online_time,
       mid_dohko_item_score_detail.avg_duration,
       mid_dohko_item_score_detail.technology_level
FROM mid_dohko_item_score_detail
WHERE mid_dohko_item_score_detail.stat_version = ((SELECT "max"(mid_dohko_item_score_detail.stat_version) AS "max"
                                                   FROM mid_dohko_item_score_detail));

alter table public.mid_dohko_item_score_detail_view owner to awsuser;

grant select on public.mid_dohko_item_score_detail_view to gv_ro;

grant select on public.mid_dohko_item_score_detail_view to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.mid_dohko_item_score_detail_view to gv_online_rw;

grant select on public.mid_dohko_item_score_detail_view to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.mid_dohko_item_score_detail_view to gv_offline_rw;

grant select on public.mid_dohko_item_score_detail_view to gv_alert;

grant select on public.mid_dohko_item_score_detail_view to dev_user;

