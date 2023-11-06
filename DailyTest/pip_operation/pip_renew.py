import pkg_resources
from subprocess import call

for package in [dist.project_name for dist in pkg_resources.working_set]:
    command = 'pip install --force-reinstall ' + str(package)
    print(command)
    call(command, shell=True)

