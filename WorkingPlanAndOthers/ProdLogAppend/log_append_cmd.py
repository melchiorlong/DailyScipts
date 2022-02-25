from datetime import datetime

date = datetime.utcnow().strftime('%Y%m%d')
path = "/Users/long.tian/PycharmProjects/personal_tianlong_server/WorkingPlanAndOthers/ProdLogAppend/log_list.txt"

muid = 'db2dc004'

cmd_list = []
log_list = []
with open(path, 'r') as file:
    log_name = file.readlines()
    log_list.append(log_name)

for log_fac in log_list[0]:
    log_name = log_fac.replace('\n', '')
    cmd = f'zcat /var/logs/{log_name} | grep {muid} >> /tmp/log{date}_{muid}.txt'
    cmd_list.append(cmd)

init_cmd = f'> /tmp/log{date}_{muid}.txt'
current_log_cmd = f'cat /var/logs/gvcommon_gateway.log | grep {muid} >> /tmp/log{date}_{muid}.txt'

print('')
print('========================================================================')
print('ls /var/logs/ | grep gateway')
print('========================================================================')
print(init_cmd)
for cmd in cmd_list:
    print(cmd)
print(current_log_cmd)
print('========================================================================')
