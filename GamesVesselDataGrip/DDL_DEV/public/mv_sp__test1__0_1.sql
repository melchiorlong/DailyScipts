create procedure public.mv_sp__test1__0_1(start_xid bigint, end_xid bigint, recompute boolean, finished_xid_list character varying)
	language plpgsql
as $$
BEGIN CREATE TABLE public.mv_tbl__test1__0__tmp BACKUP YES AS (
SELECT TRUNC(DATE_ADD(CAST('hour' AS TEXT), CAST(8 AS INT4), "kch_saori_gp_install_info"."date_occurred")) AS "trunc", CASE WHEN "kch_saori_gp_install_info"."media_source" IS NULL THEN CAST('null' AS VARCHAR) ELSE "kch_saori_gp_install_info"."media_source" END AS "media_source", CASE WHEN "kch_saori_gp_install_info"."campaign_id" IS NULL THEN CAST('null' AS VARCHAR) ELSE "kch_saori_gp_install_info"."campaign_id" END AS "campaign_id", CASE WHEN "kch_saori_gp_install_info"."country_code" IS NULL THEN CAST('null' AS VARCHAR) ELSE "kch_saori_gp_install_info"."country_code" END AS "country_code", COUNT(DISTINCT "kch_saori_gp_install_info"."kochava_device_id") AS "count" FROM "public"."kch_saori_gp_install_info" AS "kch_saori_gp_install_info" GROUP BY TRUNC(DATE_ADD(CAST('hour' AS TEXT), CAST(8 AS INT4), "kch_saori_gp_install_info"."date_occurred")), "kch_saori_gp_install_info"."media_source", "kch_saori_gp_install_info"."campaign_id", "kch_saori_gp_install_info"."country_code"
);CREATE OR REPLACE VIEW  public.test1 AS SELECT * FROM public.mv_tbl__test1__0__tmp;DROP TABLE public.mv_tbl__test1__0;ALTER TABLE public.mv_tbl__test1__0__tmp RENAME TO mv_tbl__test1__0;CREATE OR REPLACE VIEW public.test1 AS SELECT * FROM public.mv_tbl__test1__0; END;
$$;

