from datetime import datetime
from rock.s3.s3_proxy import S3Proxy


def classify_s3_init(bucket, s3_dst: str):
    # 为了保证 classify 能够重复运行，所以需要插入前初始化
    if s3_dst:
        # print(s3_dst)


        s3p = S3Proxy(
            bucket=bucket,
            aws_access_key_id='AKIAWXPN5MB5XNQ4ZSGN',
            aws_secret_access_key='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',
            region_name='us-east-1',
            endpoint_url='https://s3.amazonaws.com',
        )
        key_list_all = s3p.list_key(s3_dst)
        # 有则删除，无则pass
        if key_list_all:
            for key in key_list_all:
                print(key)
                # s3p.remove_file(key)


log_hour = datetime.strptime('2022-03-01T12', "%Y-%m-%dT%H")

classify_s3_init(
    bucket='ec2.gvprod.logs',
    s3_dst="{}/{}/{:02d}/{:02d}/{:02d}".format(
        'gv-datahouse/classify/behaviorevent/painting',
        log_hour.year,
        log_hour.month,
        log_hour.day,
        log_hour.hour,
    ),
)


# 's3://ec2.gvprod.logs/gv-datahouse/classify/'