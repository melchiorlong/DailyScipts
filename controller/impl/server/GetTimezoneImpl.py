from controller.time.get_timezone import GetTimezone
from datetime import datetime, timezone, timedelta


class GetTimezoneImpl(GetTimezone):

    def get_time_zone(self, time_zone):
        result = {
            "meta": {
                "code": 200,
            },
            "data": {
                "server_time": datetime.now(tz=timezone(timedelta(hours=0))).strftime('%Y-%m-%dT%H:%m:%S'),
                "target_time": datetime.now(tz=timezone(timedelta(hours=int(time_zone)))).strftime('%Y-%m-%dT%H:%m:%S')
            }

        }
        return result
