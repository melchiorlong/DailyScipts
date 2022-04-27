import os

ab_path = '/Users/long.tian/PycharmProjects/GV_Lib/dag_prod_new_airflow_server'

dag_name_list = []

for dirpath, dirnames, filenames in os.walk(ab_path):
    for filename in filenames:
        if filename.endswith('.py'):
            file_path = os.path.join(dirpath, filename)
            # print(file_path)
            with open(file_path) as f:
                lines = f.readlines()
                dag_name = ""
                schedule_interval = ""
                dag_map = {}

                for line in lines:
                    if line.strip().startswith('dag_name'):
                        dag_name = line.split("'")[1]
                        dag_map['dag_name'] = dag_name
                        dag_map['file_path'] = file_path
                    if line.strip().startswith('schedule_interval'):
                        line_temp = line.strip().replace('/n', '')
                        schedule_interval = line_temp
                        dag_map['schedule_interval'] = schedule_interval

                dag_name_list.append(dag_map)

dag_name_list = filter(None, dag_name_list)
print("dag_name\tschedule_interval")
for dag_map in dag_name_list:
    name = dag_map['dag_name']
    file_path = dag_map['file_path']
    schedule = dag_map['schedule_interval'].split("'")[1] if 'None' not in dag_map['schedule_interval'] else 'None'
    print(file_path+ '\t' + name + '\t' + schedule)
