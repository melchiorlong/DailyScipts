from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from rock.common import log


logger = log.get_logger('prod2stage')


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


engine = create_engine('postgresql://gv_developer:AjFtinLDMQ0w7i0f@3.230.194.153:5200/db_redshift_gv')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))()

sql_list = [
    """
    unload ('select * from {tb}') to 's3://gvprod/tmp/redshift/data_sync/{date}/{tb_name}/data'
    iam_role 'arn:aws:iam::462744805499:role/redshift-s3-rw'
    format as parquet
    allowoverwrite
    """.format(
        tb=tb,
        tb_name=tb.split(' ', 1)[0],
        date=str(datetime.utcnow().date())
    )
    for tb in [
        "mid_dh_ua_data",
        "dim_poseidon_campaign_info",
        "stat_kch_install_retention_count",
        "ads_posd_kch_retention_activities",
        "mid_ilrd_campaign_roi_total_rev",
        # "dws_ua_muid_campaign_detail",
        # "stat_kch_install_retention_count",
        # "mid_ilrd_campaign_roi_total_rev",
        # "mid_dh_ua_data",
        # "dim_poseidon_campaign_info",
        # 'dim_poseidon_campaign_info',
        # 'stat_kch_install_retention_count',
        # 'temp_mid_ilrd_campaign_roi_total_rev_new'
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