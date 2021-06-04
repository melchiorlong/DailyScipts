from controller.time.server.get_server_time import GetServerTime
from datetime import datetime, timezone, timedelta


class GetServerTimeImpl(GetServerTime):

    def get_time_now(self):
        result = {
            "meta": {
                "code": 200,
            },
            "data": {
                "server_time": datetime.now(tz=timezone(timedelta(hours=0))).strftime('%Y-%m-%dT%H:%m:%S')
            }

        }
        return result
