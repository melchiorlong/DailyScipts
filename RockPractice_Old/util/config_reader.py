import yaml

_yaml_path = '/Users/long.tian/PycharmProjects/RockPractice/config.yaml'

def get_config():

    with open(_yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        return data