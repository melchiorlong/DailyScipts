from datetime import datetime, timedelta
import time
import paramiko


def task_run(muid, start_time_str, end_time_str=None, factor_list=None):
    filter_factors_str = ""
    if factor_list:
        factors = list(filter(None, factor_list))
        filter_factors_str = " ".join(
            "| grep {}".format(
                fac
            ) for fac in factors
        )

    start_time = datetime.strptime(start_time_str, '%H-%M') + timedelta(hours=-8)

    if end_time_str:
        end_time = datetime.strptime(end_time_str, '%H-%M') + timedelta(hours=-8)
    else:
        end_time_HM = datetime.utcnow().strftime('%H-%M')
        end_time = datetime.strptime(end_time_HM, '%H-%M')

    date = datetime.utcnow().strftime('%Y%m%d')
    cmd_list = []
    init_cmd = f'> /tmp/log{date}_{muid}.txt'
    current_log_cmd = f'cat /var/logs/gvcommon_gateway.log | grep {muid} {filter_factors_str} >> /tmp/log{date}_{muid}.txt'

    ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(key)
    ssh.connect(
        hostname='3.230.194.153',
        username='ubuntu',
        key_filename='/Users/long.tian/.ssh/key-gv-prod-admin.pem',
        timeout=120
    )

    stdin, stdout, stderr = ssh.exec_command('ls /var/logs/*.gz | grep gateway')
    new_log_list = []
    index = 0
    for lines in stdout:
        log_name = lines.replace('\n', '')
        if len(log_name) < 51:
            continue
        log_time_str = log_name[40:48]
        log_time = datetime.strptime(log_time_str, '%H-%M-%S')
        if log_time >= end_time:
            continue
        if log_time <= start_time:
            index += 1
        new_log_list.append(lines.replace('\n', ''))

    for name in new_log_list[index - 1:]:
        cmd = f'zcat {name} | grep {muid} {filter_factors_str} >> /tmp/log{date}_{muid}.txt'
        cmd_list.append(cmd)

    final_cmd_list = []
    final_cmd_list.append(init_cmd)
    for cmd in cmd_list:
        final_cmd_list.append(cmd)
    if not end_time_str:
        final_cmd_list.append(current_log_cmd)

    cmd_str = ";".join(final_cmd_list)
    try:
        ssh.exec_command(cmd_str)
        print(cmd_str)
        time.sleep(2)
    except Exception as e:
        s = str(e)
        print(s)
    finally:
        ssh.close()


task_run(
    muid='9a698070',
    start_time_str='11-10',
    # factor_list=['Poseidon', '', ''],
    # end_time_str='11-43',
)
