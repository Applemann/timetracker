#!/usr/bin/env python

from datetime import datetime
import sys, re
import os.path


#CONFIG_PATH='/home/martin/.timetrack'
CONFIG_PATH='config'

TIME_TRACK_FILE='%s/martin_%s.tm' % (CONFIG_PATH, datetime.now().strftime("%Y-%m"))
TIME_TRACK_JSON='%s/martin_%s.json' % (CONFIG_PATH, datetime.now().strftime("%Y-%m"))
#TIME_TRACK_FILE=TIME_TRACK_JSON
TIME_TRACK_STATUS='%s/status' % CONFIG_PATH




### SHOW TIMES
def show_times():
    file = open(TIME_TRACK_FILE)
    timetracks = file.read()
    file.close()
    timelines = timetracks.split('\n')
    total_hour = 0
    total_minute = 0

    for timeline in timelines[-5:]:
        timeline = timeline.split('#')
        date = timeline[0]

        if not len(timeline) > 1: 
            continue

        sum_hour = 0
        sum_minute = 0

        print '#'*30
        print ''
        print date+':\n'
        for time in timeline[1:]:
            try:
                times = time.split('|')
                message = re.split('[{}]', times[1])[1]#.index('{')
                #print re.split('[{}]', times[1])
                #print times
                times[1] = times[1].split('{')[0]

                if times[1] == '':
                    times[1] = datetime.now().strftime("%H:%M") 

                hour = int(times[1].split(':')[0]) - int(times[0].split(':')[0])
                minute = int(times[1].split(':')[1]) - int(times[0].split(':')[1])
                sum_hour += hour
                sum_minute += minute
                if minute < 0:
                    hour -= 1
                    minute += 60
                if minute < 10:
                    minute = "0"+str(minute)

                if times[1] == datetime.now().strftime("%H:%M"):
                    times[1] = 'now'
                print '\t'+times[0]+"|"+times[1]+'\t'+str(hour)+":"+str(minute)+"\t"+message
            except:
                pass


            if sum_minute < 0:
                sum_hour -= 1
                sum_minute += 60

        print '-'*30
        if sum_minute < 10:
            sum_minute = "0"+str(sum_minute)
        print 'Odpracovany cas:\t'+str(sum_hour)+":"+str(sum_minute)
        print '\n'

        total_hour += sum_hour
        total_minute += int(sum_minute)
        total_hour += total_minute/60
        total_minute = total_minute%60


    if total_minute < 10:
        total_minute = "0"+str(total_minute)
    print 'Total:\t\t\t'+str(total_hour)+":"+str(total_minute)
        

def get_last_day():
    file = open(TIME_TRACK_FILE)
    timetracks = file.read()
    timelines = timetracks.split('\n')
    while '' in timelines: 
        timelines.remove('')

    file.close()
    return timelines[-1].split('#')


### INPUT TIME
def input_time(status, message=''):
    file = open(TIME_TRACK_FILE, 'a')

    now_day = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M")

    last_day = get_last_day()

    if status == 'entry':
        if last_day[0] == now_day:
            file.write("#%s|" % (now_time,))
        else:
            file.write("\n%s#%s|" % (now_day, now_time))

    if status == 'leave':
        if last_day[0] == now_day:
            file.write("%s{%s}" % (now_time, message))
        else:
            file.write("\n%s#|%s{%s}" % (now_day, now_time, message))

    file.close()
    show_times()

def set_status(status):
    with open(TIME_TRACK_STATUS, 'w') as tt_status:
        tt_status.write(status)

def get_status():
    with open(TIME_TRACK_STATUS, 'r') as timetrack_status:
        return timetrack_status.read().split('\n')[0]





if not os.path.exists(TIME_TRACK_FILE):
    now_day = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M")
    with open(TIME_TRACK_FILE, 'w') as timetrack_file:
        timetrack_file.write("\n"+now_day+"#"+now_time+"|")
    set_status('0')
    show_times()
    
if len(sys.argv)>1:
    if sys.argv[1]=='in':
        if get_status() == '1':
            input_time('entry')
            set_status('0')
    if sys.argv[1]=='out':
        message = ''
        if sys.argv[2]=='-m':
            message = sys.argv[3]
        if get_status() == '0':
            input_time('leave', message)
            set_status('1')



    if sys.argv[1]=='status':
        show_times()
    if sys.argv[1]=='src' or sys.argv[1]=='source':
        os.system('cat '+TIME_TRACK_FILE)

else:
    show_times()
