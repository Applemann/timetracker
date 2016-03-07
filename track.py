#!/usr/bin/env python

from datetime import datetime
import sys, re
import os.path
import json
import collections


#CONFIG_PATH='/home/martin/.timetrack'
CONFIG_PATH='config'

TIME_TRACK_FILE='%s/martin_%s.tm' % (CONFIG_PATH, datetime.now().strftime("%Y-%m"))
#TIME_TRACK_JSON='%s/martin_%s.json' % (CONFIG_PATH, datetime.now().strftime("%Y-%m"))
TIME_TRACK_JSON='%s/timetrack.json' % CONFIG_PATH
TIME_TRACK_FILE=TIME_TRACK_JSON
TIME_TRACK_STATUS='%s/status' % CONFIG_PATH


def get_now_date():
    return datetime.now().strftime("%Y-%m-%d")

def get_now_time():
    return datetime.now().strftime("%H:%M")


def save_timetrack(timetrack):
    now_day = get_now_date()
    tm = get_timetrack()
    tm[now_day] = timetrack
    file = open(TIME_TRACK_JSON, 'w')
    file.write(json.dumps(tm)) 
    file.close()

def get_timetrack(date=None):
    file = open(TIME_TRACK_JSON)
    timetrack = json.loads(file.read())
    file.close()

    if date != None:
        if date in timetrack:
            return timetrack[date]
        else:
            return timetrack['2016-3-3']

    return collections.OrderedDict(sorted(timetrack.items()))




## SHOW TIMES
def show_times():
    timetrack = get_timetrack()

    timeline = ''
    message = ''
    total_hour = 0
    total_minute = 0

    for date in timetrack:
        timeline = timetrack[date]['tracking']
        message = timetrack[date]['message']

        if not len(timeline) > 1: 
            continue

        sum_hour = 0
        sum_minute = 0

        print '#'*30
        print ''
        print date+':\n'
        for time in timeline:
            try:
                times = time.split('|')
                #message = re.split('[{}]', times[1])[1]#.index('{')
                #print re.split('[{}]', times[1])
                #print times
                #times[1] = times[1].split('{')[0]

                if times[1] == '':
                    times[1] = get_now_time()

                hour = int(times[1].split(':')[0]) - int(times[0].split(':')[0])
                minute = int(times[1].split(':')[1]) - int(times[0].split(':')[1])
                sum_hour += hour
                sum_minute += minute
                if minute < 0:
                    hour -= 1
                    minute += 60
                if minute < 10:
                    minute = "0"+str(minute)

                if times[1] == get_now_time():
                    times[1] = 'now'
                print '\t'+times[0]+"|"+times[1]+'\t'+str(hour)+":"+str(minute)
            except:
                pass


            if sum_minute < 0:
                sum_hour -= 1
                sum_minute += 60

        print '-'*30
        if sum_minute < 10:
            sum_minute = "0"+str(sum_minute)
        print 'Odpracovany cas:\t'+str(sum_hour)+":"+str(sum_minute)+"\t"+message
        print '\n'

        total_hour += sum_hour
        total_minute += int(sum_minute)
        total_hour += total_minute/60
        total_minute = total_minute%60


    if total_minute < 10:
        total_minute = "0"+str(total_minute)
    print 'Total:\t\t\t'+str(total_hour)+":"+str(total_minute)
        


### INPUT TIME
def input_time(status, message=''):
    now_day = get_now_date()
    timetrack = get_timetrack(date=now_day)
    tracking = timetrack['tracking']
    timetrack['message'] += message


    now_time = get_now_time()


    if status == 'entry':
        tracking.append("%s|" % (now_time,))
        print tracking

    if status == 'leave':
        tracking[len(tracking)-1] += now_time
        print tracking


    save_timetrack(timetrack)

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
#    with open(TIME_TRACK_FILE, 'w') as timetrack_file:
#        timetrack_file.write("\n"+now_day+"#"+now_time+"|")
    set_status('0')
    show_times()
    
if len(sys.argv)>1:
    if sys.argv[1]=='in':
        if get_status() == '1':
            input_time('entry')
            set_status('0')
    if sys.argv[1]=='out':
        message = ''
        try:
            if sys.argv[2]=='-m':
                message = sys.argv[3]
        except:
            pass
        if get_status() == '0':
            input_time('leave', message)
            set_status('1')



    if sys.argv[1]=='status':
        show_times()
    if sys.argv[1]=='src' or sys.argv[1]=='source':
        print TIME_TRACK_JSON
        os.system('cat '+TIME_TRACK_JSON)

else:
    show_times()
