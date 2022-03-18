create table public.puzzle_log
(
	log_date varchar(16),
	muid varchar(64) distkey,
	app_package_name varchar(64),
	platform varchar(16),
	app_version_code integer encode az64,
	country varchar(64),
	action_time timestamp encode az64,
	ip varchar(64),
	timezone double precision,
	user_segment varchar(32),
	action_type varchar(32),
	img_id varchar(32),
	ratio varchar(32),
	piece integer encode az64,
	is_rotated varchar(8),
	is_local varchar(8),
	topic_id varchar(32),
	topic_thumb_id integer encode az64,
	topic_price integer encode az64,
	topic_img_count integer encode az64,
	location varchar(32),
	duration integer encode az64,
	canvas_id integer encode az64,
	success varchar(8),
	previous_value integer encode az64,
	current_value integer encode az64,
	hint_eye_count integer encode az64,
	hint_frame_count integer encode az64,
	coin_change_type integer encode az64,
	coin_change_reason varchar(64),
	bonus integer encode az64,
	this_consume_column_filling integer encode az64,
	this_consume_line_filling integer encode az64,
	this_consume_area_filling integer encode az64,
	this_consume_blank_filling integer encode az64,
	this_consume_easy_piece integer encode az64,
	this_by_coin_column_filling integer encode az64,
	this_by_coin_line_filling integer encode az64,
	this_by_coin_area_filling integer encode az64,
	this_by_coin_blank_filling integer encode az64,
	this_by_coin_easy_piece integer encode az64,
	this_by_ad_column_filling integer encode az64,
	this_by_ad_line_filling integer encode az64,
	this_by_ad_area_filling integer encode az64,
	this_by_ad_blank_filling integer encode az64,
	this_by_ad_easy_piece integer encode az64,
	previous_prop_column_filling integer encode az64,
	previous_prop_line_filling integer encode az64,
	previous_prop_area_filling integer encode az64,
	previous_prop_blank_filling integer encode az64,
	previous_prop_easy_piece integer encode az64,
	current_prop_column_filling integer encode az64,
	current_prop_line_filling integer encode az64,
	current_prop_area_filling integer encode az64,
	current_prop_blank_filling integer encode az64,
	current_prop_easy_piece integer encode az64,
	this_by_luckypiece_free_column_filling integer encode az64,
	this_by_luckypiece_free_line_filling integer encode az64,
	this_by_luckypiece_free_area_filling integer encode az64,
	this_by_luckypiece_free_blank_filling integer encode az64,
	this_by_luckypiece_free_easy_piece integer encode az64,
	this_consume_free_column_filling integer encode az64,
	this_consume_free_line_filling integer encode az64,
	this_consume_free_area_filling integer encode az64,
	this_consume_free_blank_filling integer encode az64,
	this_consume_free_easy_piece integer encode az64,
	special_hint_show integer encode az64,
	special_hint_click integer encode az64,
	prop_change_reason varchar(32)
)
sortkey(log_date);

alter table public.puzzle_log owner to gv_root;

grant select on public.puzzle_log to gv_ro;

grant select on public.puzzle_log to gv_online_ro;

grant select on public.puzzle_log to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.puzzle_log to gv_online_rw;

grant delete, insert, references, select, trigger, update on public.puzzle_log to gv_offline_rw;

grant select on public.puzzle_log to metabase;

grant select on public.puzzle_log to gv_developer;

