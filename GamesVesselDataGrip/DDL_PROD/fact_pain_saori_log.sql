create external table spectrum.fact_pain_saori_log
(
	muid varchar(64),
	app_package_name varchar(64),
	platform varchar(16),
	app_version_code int,
	country varchar(8),
	user_segment varchar(32),
	action_time int,
	ip varchar(64),
	timezone double,
	painting_item_id varchar(64),
	action_type varchar(16),
	src varchar(32),
	position varchar(32),
	lock_flag int,
	is_test varchar(8),
	duration int,
	hint_count int,
	path_id varchar(32),
	color_name varchar(16),
	hint_type int,
	hint_left int,
	color_left int,
	recommend_item_id varchar(32),
	start int,
	thumb_index varchar(4),
	marketing_name varchar(64),
	network_status varchar(16),
	"end" int
)
partitioned by (log_time timestamp)
row format serde 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
with serdeproperties('serialization.format'='1')
stored as
inputformat 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat'
outputformat 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
location 's3://gvprod/data_warehouse/painting/fact_table/behavior';

