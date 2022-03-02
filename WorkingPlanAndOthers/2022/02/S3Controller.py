from rock.s3.s3_proxy import S3Proxy

s3p = S3Proxy(
    bucket='gvprod',
    aws_access_key_id='AKIAWXPN5MB5V4YEBTG5',
    aws_secret_access_key='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',
    region_name='us-east-1',
    endpoint_url='https://s3.amazonaws.com',
)

# suffix_list = [
#     'devops/dw/ua_export/google/uac3/2022-02-22/aiolos_gp/',
# ]

# dir_prefix = 'data_warehouse/poseidon/'

# new_log_p_list = []
# for r in res:
#     if r.startswith('log_time='):
#         final_dir = dir_prefix + r
#         new_log_p_list.append(final_dir)

# del_key_list = []
# for fd in suffix_list:
#     path = dir_prefix + fd
#     res = s3p.list_key(
#         s3_prefix=path
#     )
#     for r in res:
#         suf = r[52:]
#         if suf.startswith('/202202') or suf.startswith('/data/202202'):
#             # print(r)
#             # s3p.remove_file(r)
#             print(r + ' Deleted!')


# s3://gvprod/data_warehouse/poseidon_backfill/log_time=2022-02-25 08:00:00/


# for su in suffix_list:
#     csv_dir = s3p.list_key(su)
#     for csv in csv_dir:
#         s3p.download_file_if_exists(csv, f'/Users/long.tian/Downloads/11.csv')


execute_date = '2022-02-28 17:00:00'
dst_s3_prefix = 'data_warehouse/poseidon'
dst_s3_dir = dst_s3_prefix + '/log_time=' + execute_date
key_list_all = s3p.list_key(dst_s3_dir)
# 由于只能通过parquet名称区分Psd和PsdV2的日志文件 所以只能这么写
key_list_extend_aws_key = []
for key in key_list_all:
    file_name = key.split('/')[-1]
    if not file_name.startswith('part'):
        if file_name == '_SUCCESS':
            continue
        key_list_extend_aws_key.append(key)
try:
    if len(key_list_extend_aws_key) > 0:
        for key in key_list_extend_aws_key:
            # s3p.remove_file(key)
            print(key)
except Exception as exception:
    raise
