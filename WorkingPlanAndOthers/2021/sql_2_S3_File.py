from rock.common import init_rockenv
init_rockenv()


from datetime import datetime
from uuid import uuid4

from rock_sccommon.s3 import S3Proxy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from rock.common import log


logger = log.get_logger('sc')


engine = create_engine('postgresql://gv_developer:AjFtinLDMQ0w7i0f@3.230.194.153:5200/db_redshift_gv')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))()


select_sql = """
With install_user as (
SELECT muid_dimension.muid,
                kch_install.country_code,
                trunc(kch_install.date_occurred) as install_date
FROM kch_aiolos_gp_install_info as kch_install
JOIN muid_dimension 
on kch_install.kochava_device_id = muid_dimension.kch_id
where trunc(date_occurred) <='2021-07-12'
            and trunc(date_occurred) >='2021-06-12'
                     and kch_install.country_code in ('BR','MX','IN','AR','CO')
                     and app_version = 10 
order by 3
),
initial_process_table as( 
SELECT  muid,
                trunc(action_time) as ac_date,
                current_value,
                previous_value,
                action_time,
                coin_change_type,
                coin_change_reason,
                current_value - previous_value as diff_value,
                rank() over( partition by ac_date,muid order by action_time desc) as ex_balance_rank
FROM puzzle_log
WHERE ac_date>='2021-06-12'
            and ac_date<='2021-07-12'
            and coin_change_type in (1,2)
                     and platform='android'
                     and app_version_code=10
order by 2,1
),
revenue_spend_table as (
SELECT muid,
       ac_date,
       sum(case when coin_change_type=1 then diff_value else 0 end) as muid_revenue,
       sum(case when coin_change_type=2 then abs(diff_value) else 0 end ) as muid_spend
from initial_process_table
group by muid, ac_date
),
revenue_spend_transition_table as (
SELECT 
       ins.muid,
       ins.install_date,
       rs.ac_date,
       ins.country_code,
       rs.muid_revenue,
       rs.muid_spend,
       datediff(day,ins.install_date,rs.ac_date) as retention_day
from install_user as ins
join revenue_spend_table as rs 
on ins.muid = rs.muid
)
SELECT * from revenue_spend_transition_table
""".replace("'", "''")

s3_key = 'tmp/redshift/data_export/{date}/{uuid}/data'.format(
    date=str(datetime.utcnow().date()),
    uuid=uuid4().hex
)
unload_sql = """
    unload ('{select_sql}') to 's3://gvprod/{s3_key}'
    iam_role 'arn:aws:iam::462744805499:role/redshift-s3-rw'
    allowoverwrite header parallel off
    format as csv
""".format(
    select_sql=select_sql,
    s3_key=s3_key
)

try:
    logger.info("start")
    import time
    s = time.time()
    session.execute(unload_sql)
    session.commit()
    s3_proxy = S3Proxy()
    file_url = s3_proxy.get_object_presigned_url(s3_key + '000', expiration=3600*24*3)
    e = time.time()
    print('file_url', file_url)
    logger.info('success', e - s)
except Exception as e:
    session.rollback()
    logger.traceback()
    s = str(e)
    print(s)