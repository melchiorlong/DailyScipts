from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from rock.common import log



sql_list = [
    """
    delete from {tb_name};
    copy {tb_name} from 's3://gvdev/tmp/redshift/data_sync/{date}/{tb_name}/data'
    iam_role 'arn:aws:iam::149870400580:role/redshift-s3-rw'
    format as parquet
        """.format(
        tb=tb,
        tb_name=tb.split(' ', 1)[0],
        date=str(datetime.utcnow().date())
    )
    for tb in [
        "puzzle_log where trunc(action_time) >= ''2021-06-10''",
        "kch_aiolos_gp_install_info where trunc(date_occurred) >= ''2021-06-10''",
        "kch_aiolos_ip_install_info where trunc(date_occurred) >= ''2021-06-10''",
        "muid_dimension",
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

for i in sql_list:
    print(i)
    print('------------------')

