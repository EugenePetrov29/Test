import psutil, os, csv, datetime
import pandas as pd
import time

time_value = int(input('Введите интервал сбора данных в секундах: '))
is_first_iter = True

while True:
    today = datetime.datetime.now()
    date = today.strftime("%Y-%m-%d")
    t = today.strftime("%H:%M:%S")

    f = open('/proc/sys/fs/file-nr', 'r')
    desk = ''
    for i in f.read():
        if i == '\t':
            break
        desk += i

    cpu = str(psutil.cpu_percent(interval=1)) + '%'
    rss = str(round(int(psutil.virtual_memory()[5])/1000000, 2)) + 'Mb'
    vsz = str(round(int(psutil.virtual_memory()[0])/1000000, 2)) + 'Mb'

    dict_sys = ({
        'Date' : date,
        'Time' : t,
        'CPU' : cpu,
        'RSS' : rss,
        'VSZ' : vsz,
        'Allocated_descriptors' : desk
    }, )

    df = pd.DataFrame.from_dict(dict_sys, orient='columns')
    if is_first_iter == True:
        df.to_csv('./sys.csv', mode='a', index=False)
    else:
        df.to_csv('./sys.csv', mode='a', header=False, index=False)
    is_first_iter = False
    print(dict_sys)
    time.sleep(time_value - 1)