import datetime

time1 = datetime.datetime.strptime('2021-03-11 16:33:47', "%Y-%m-%d %H:%M:%S")
time2 = datetime.datetime.strptime(str(datetime.datetime.now()).split('.')[0], "%Y-%m-%d %H:%M:%S")
print(time2)

fifteen_min = datetime.timedelta(minutes=15)

print(fifteen_min < datetime.datetime.now() - time1)