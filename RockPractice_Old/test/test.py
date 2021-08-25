from datetime import datetime, timezone, timedelta
from RockPractice_Old.util import config_reader

datetime.now().strftime('%Y-%m-%dT%H:%m:%S')
datetime.now(tz=timezone(timedelta(hours=8))).strftime('%Y-%m-%dT%H:%m:%S')
datetime.now(tz=timezone(timedelta(hours=8))).strftime('%Y-%m-%dT%H:%m:%S')

print(config_reader.get_config().get('user_blacklist'))

