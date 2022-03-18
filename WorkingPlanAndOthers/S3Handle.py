from rock.s3.s3_proxy import S3Proxy

s3p = S3Proxy(
    bucket='gvprod',
    aws_access_key_id='AKIAWXPN5MB5V4YEBTG5',
    aws_secret_access_key='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',
    region_name='us-east-1',
    endpoint_url='https://s3.amazonaws.com',
)

s3_prefix = 'data_warehouse/oil_painting/fact_table/behavior/log_time='

key_list_all = s3p.list_key(s3_prefix)

key_list_extend_aws_key = []
for key in key_list_all:
    file_name = key.split('/')[-1]
    if not file_name.startswith('part'):
        if file_name == '_SUCCESS':
            continue
        key_list_extend_aws_key.append(key)
    try:
        if len(key_list_extend_aws_key) > 0:
            for s3_key in key_list_extend_aws_key:
                # s3p.remove_file(s3_key)
                print(s3_key + " Deleted! ")
    except Exception as exception:
        raise exception
