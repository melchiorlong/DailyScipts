from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from rock.common import log


logger = log.get_logger('dev2stage')


def _is_dml(sql_statement):
    """
    判断是不是操作性sql
    :return:
    """
    for key_word in ['cancel', 'unload', 'copy', 'into', 'create', 'alter', 'drop', 'grant', 'revoke', 'insert',
                     'delete', 'update']:  # 暂时先只进行简单判断，更复杂的判断逻辑后续再考虑
        if key_word in sql_statement.lower():
            return True
    return False


engine = create_engine('postgresql://awsuser:bYPoGonCjqlee5WNj@redshift-cluster-2.cltonxgv2obv.us-east-1.redshift.amazonaws.com:5439/db_redshift_dev')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))()

sql_list = [
    """
    unload ('select * from {tb}') to 's3://gvdev/tmp/redshift/data_sync/{date}/{tb}/data'
    iam_role 'arn:aws:iam::149870400580:role/redshift-s3-rw'
    format as parquet
    allowoverwrite
    """.format(
        tb=tb,
        tb_name=tb.split(' ', 1)[0],
        date=str(datetime.utcnow().date())
    )
    for tb in [
        "stat_poseidon_coin_analysis_balance",
        "stat_poseidon_coin_analysis_revenue_cost",
        "stat_poseidon_coin_analysis_revenue_cost_summary",
        # "muid_dimension",
        # 'dim_poseidon_campaign_info',
        # 'stat_kch_install_retention_count',
        # 'mid_poseidon_retention_lt',
        # 'mid_ilrd_quality_check_poseidon',
        # 'mid_ilrd_quality_check_dau',
        # 'mid_poseidon_day_roi_summary',
        # 'mid_poseidon_day_ad_revenue',
        # 'mid_poseidon_day_retention_and_roi',
        # 'mid_poseidon_day_dau_dnu',
        # 'mid_ilrd_campaign_roi_total_rev'
    ]
]

try:
    logger.info("start")
    import time

    s = time.time()
    for sql in sql_list:
        rs = session.execute(sql)
        if not _is_dml(sql):
            rs = rs.fetchall()
            for r in rs:
                print(r)
        else:
            print(rs)
        session.commit()
    e = time.time()
    logger.info('success', e - s)
except Exception as e:
    session.rollback()
    logger.traceback()
    s = str(e)
    print(s)
