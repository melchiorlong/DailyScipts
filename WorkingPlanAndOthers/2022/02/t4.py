from rock.s3 import S3Proxy
import datetime

local_path = f'/Users/long.tian/PycharmProjects/personal_tianlong_server/WorkingPlanAndOthers/ProdLogAppend/test.txt'


date_time = datetime.datetime.strptime('2022-02-21 06:00:00', '%Y-%m-%d %H:%M:%S')

log_time = date_time.strftime('%Y-%m-%d %H:%M:%S')

# dst_path = "s3://{bucket}/{prefix}/log_time={log_time}".format(
#     bucket='gvprod',
#     prefix='data_warehouse/poseidon_v2',
#     log_time=log_time,
# )


dst_path = 's3://gvprod/data_warehouse/poseidon_v2/log_time=2022-02-21 06:00:00'

# l1 = dst_path.split('://')[1]
s2 = '/'.join(dst_path.split('://')[1].split('/')[1:])
# s2 = '/'.join(l1.split('/')[1:])

print(s2)



#
# index1 = dst_path.find('://')
# path_temp = dst_path[index1 + 3]
# index2 = dst_path[index1 + 3].index('/')
# s3_suffix = dst_path[index1 + index2 + 3 + 1:]
# print(s3_suffix)
#





#
# s3p = S3Proxy(
#     bucket='gvprod',
#     aws_access_key_id='AKIAWXPN5MB5V4YEBTG5',
#     aws_secret_access_key='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',
#     region_name='us-east-1',
#     endpoint_url='https://s3.amazonaws.com',
# )
#
# key_list = s3p.list_key(dst_path)
# if len(key_list) > 0:
#     for key in key_list:
#         s3p.remove_file(key)
#
#




