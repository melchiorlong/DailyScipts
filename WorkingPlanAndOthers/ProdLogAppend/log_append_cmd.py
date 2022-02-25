from datetime import datetime, timedelta
import time
import paramiko


def task_run(muid, start_time_str):
    date = datetime.utcnow().strftime('%Y%m%d')

    cmd_list = []
    init_cmd = f'> /tmp/log{date}_{muid}.txt'
    current_log_cmd = f'cat /var/logs/gvcommon_gateway.log | grep {muid} >> /tmp/log{date}_{muid}.txt'

    ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(key)
    ssh.connect(
        hostname='3.230.194.153',
        username='ubuntu',
        key_filename='/Users/long.tian/.ssh/key-gv-prod-admin.pem',
        timeout=5
    )
    time.sleep(2)
    stdin, stdout, stderr = ssh.exec_command('ls /var/logs/*.gz | grep gateway')

    start_time = datetime.strptime(start_time_str, '%H-%M') + timedelta(hours=-8)

    new_log_list = []
    index = 0
    for lines in stdout:
        log_name = lines.replace('\n', '')
        if len(log_name) < 51:
            continue
        log_time_str = log_name[40:48]
        log_time = datetime.strptime(log_time_str, '%H-%M-%S')
        if log_time <= start_time:
            index += 1
        new_log_list.append(lines.replace('\n', ''))

    for name in new_log_list[index - 1:]:
        cmd = f'zcat {name} | grep {muid} >> /tmp/log{date}_{muid}.txt'
        cmd_list.append(cmd)

    try:
        ssh.exec_command(init_cmd)
        print(init_cmd + ' Done')

        for cmd in cmd_list:
            ssh.exec_command(cmd)
            print(cmd + ' Done')

        ssh.exec_command(current_log_cmd)
        print(current_log_cmd + ' Done')
    except Exception as e:
        s = str(e)
        print(s)
    finally:
        ssh.close()


task_run(
    muid='db2dc004',
    start_time_str='17-30'
)
