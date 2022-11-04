from datetime import datetime
from datetime import timedelta

ST_JSON = {'Appname': [], 'Program': {}, 'UseTime': {}}

ST_FIlE_NAME = 'data.json'

ST_DATE = datetime.now().strftime('%Y/%m/%d')

ST_TIME = datetime.now().strftime('%H:%M:%S')

ST_PROGRAM_DATE = {f'Runtime_{ST_DATE}': {}}

ST_PROGRAM_DATE_NAME = f'Runtime_{ST_DATE}'


def time_sum(time) -> timedelta:
    return sum(
        [
            timedelta(hours=int(ms[0]), minutes=int(ms[1]), seconds=int(ms[2]))
            for t in time
            for ms in [t.split(":")]
        ],
        timedelta(),
    )