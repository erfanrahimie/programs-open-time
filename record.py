import subprocess
import time
from datetime import datetime
import json
from structure import ST_FIlE_NAME, ST_PROGRAM_DATE_NAME, time_sum, ST_JSON, ST_PROGRAM_DATE, ST_TIME
from os import listdir


if 'data.json' in listdir():
    pass
else:
    with open('data.json', 'w') as file:
        json.dump(ST_JSON, file, indent=2)

with open('data.json', 'r') as value:
    if not value.read():
        with open('data.json', 'w') as file:
            json.dump(ST_JSON, file, indent=2)

with open('data.json', 'r') as file:
    data = json.load(file)

if data.get('Program', ST_PROGRAM_DATE):
    pass
else:
    data['Program'] = ST_PROGRAM_DATE
    data['UseTime'] = ST_PROGRAM_DATE
    with open(ST_FIlE_NAME, 'w') as file:
        file.write(json.dumps(data))

with open('data.json', 'r') as file:
    data = json.load(file)

app_name = data['Appname']

for app in app_name:
    last_use = data['UseTime'][ST_PROGRAM_DATE_NAME].get(app)
    if last_use:
        data['Program'][ST_PROGRAM_DATE_NAME].update({app: {
            'created': ST_TIME, 'updated': ST_TIME, 'using': last_use}
        })
    with open(ST_FIlE_NAME, 'w') as file:
        json.dump(data, file, indent=2)


while True:
    with open('data.json', 'r') as data:
        FILE_DATA = json.load(data)

    app_name = FILE_DATA['Appname']
    list_programs = subprocess.run('tasklist /fi "USERNAME ne NT AUTHORITY\SYSTEM" /fi "STATUS eq running"', shell=True, text=True, capture_output=True)
    for app in app_name:
        if app.lower() in list_programs.stdout.lower():
            ST_TIME = datetime.now().strftime('%H:%M:%S')
            data = FILE_DATA['Program'][ST_PROGRAM_DATE_NAME].get(app)
            if not data:
                FILE_DATA['Program'][ST_PROGRAM_DATE_NAME].update({app: {
                    'created': ST_TIME, 'updated': ST_TIME, 'using': '0:00:00'}
                })
                FILE_DATA['UseTime'][ST_PROGRAM_DATE_NAME].update({app: '0:00:00'})
            data = FILE_DATA['Program'][ST_PROGRAM_DATE_NAME].get(app)
            if data and data['created'] != 'None':
                s1 = f'{data["created"]}'
                s2 = f'{data["updated"]}'
                s3 = f'{data["using"]}'
                FMT = '%H:%M:%S'
                tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
                tdelta = time_sum([str(tdelta), s3])
                tdelta = str(tdelta)
                FILE_DATA['Program'][ST_PROGRAM_DATE_NAME][app].update({'updated': ST_TIME})
                FILE_DATA['UseTime'][ST_PROGRAM_DATE_NAME].update({app: tdelta})
            elif data and data['created'] == 'None':
                FILE_DATA['Program'][ST_PROGRAM_DATE_NAME][app].update({'created': ST_TIME, 'updated': ST_TIME})
        else:
            data = FILE_DATA['Program'][ST_PROGRAM_DATE_NAME].get(app)
            if data:
                FILE_DATA['Program'][ST_PROGRAM_DATE_NAME][app].update({'created': 'None', 'updated': 'None'})
    with open(ST_FIlE_NAME, 'w') as file:
        json.dump(FILE_DATA, file, indent=2)
    time.sleep(10)
