create external table spectrum.fact_ivt_poseidon_log
(
	log_date varchar(16),
	muid varchar(64),
	app_package_name varchar(64),
	platform varchar(16),
	app_version_code int,
	country varchar(8),
	timezone double,
	network_type varchar(32),
	action_time timestamp,
	action_id varchar(64),
	placement_name varchar(64),
	vendor varchar(64),
	ad_format varchar(64),
	ad_id varchar(80),
	ip varchar(64),
	service_log_time timestamp,
	local_datetime timestamp,
	user_segment varchar(32),
	code int,
	size int,
	ilrd_adunit_id varchar(64),
	ilrd_adunit_name varchar(64),
	ilrd_adunit_format varchar(64),
	ilrd_id varchar(64),
	ilrd_currency varchar(8),
	ilrd_demand_partner_data varchar(128),
	ilrd_publisher_revenue double,
	ilrd_network_name varchar(64),
	ilrd_network_placement_id varchar(64),
	ilrd_app_version varchar(16),
	ilrd_adgroup_id varchar(64),
	ilrd_adgroup_name varchar(64),
	ilrd_adgroup_type varchar(64),
	ilrd_adgroup_priority int,
	ilrd_country varchar(16),
	ilrd_precision varchar(32),
	action_type varchar(32)
)
partitioned by (log_time timestamp)
row format serde 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
with serdeproperties('serialization.format'='1')
stored as
inputformat 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat'
outputformat 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
location 's3://gvprod/data_warehouse/poseidon';

