#!/usr/local/bin/python
#
# TaskPaper Parser
# K. Marchand 2014
#

from datetime import datetime, timedelta
from collections import namedtuple
from dateutil import parser
import sys
import re

tpfile = sys.argv[1]

with open(tpfile, 'rb') as f:
    tplines = f.readlines()

Flagged = namedtuple('Flagged', ['type', 'taskdate', 'project', 'task'])
flaglist = []
errlist = []

project = ''

for line in tplines:
    try:
        if '@done' in line:
            continue
        #this next part does not work with 'Bulk Flow: @week\n' This is how I tag my projects as a whole.
        if ':\n' in line:
            project = line.strip()[:-1]
        if '@due' in line:
            duetag = re.search(r'\@due\((.*?)\)', line).group(1)
            taskdate = datetime.date(parser.parse(duetag))
            flaglist.append(
                Flagged('due', taskdate, project, line.strip()))
        if '@start' in line:
            starttag = re.search(r'\@start\((.*?)\)', line).group(1)
            taskdate = datetime.date(parser.parse(starttag))
            flaglist.append(
                Flagged('start', taskdate, project, line.strip()))
        if '@today' in line:
            flaglist.append(
                Flagged('today', datetime.now(), project, line.strip()))
        if '@week' in line:
            flaglist.append(
                Flagged('week', datetime.now(), project, line.strip()))
                #a taskdate of now() does not work the best for @week, but it is not used.
    except Exception, e:
        errlist.append((line, e))

today = overdue = duethisweek = startthisweek = None
today_date = datetime.date(datetime.now())

#check out http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
em_color = '\033[92m'
default_color = '\033[0m'

# print 'SUMMARY for %s [%s]' % (tpfile, str(datetime.now())[:16])
print 'SUMMARY from %s' %str(datetime.now())[:16]

print em_color+'\nTODAY\n'+default_color

for task in flaglist:
    if task.type == 'today':
        today = True
        print '\t[%s] %s' % (task.project, task.task)
    elif task.type == 'due' and today_date == task.taskdate:
        today = True
        print '\t[%s] %s' % (task.project, task.task)
if not today:
    print '\t (none)'

print '\nOVERDUE\n'

for task in flaglist:
    if task.type == 'due' and today_date > task.taskdate:
        overdue = True
        print '\t[%s] %s' % (task.project, task.task)
if not overdue:
    print '\t (none)'

print '\nDUE THIS WEEK\n'

for task in flaglist:
    weeklater = today_date + timedelta(days=7)
    if task.type == 'due' and today_date < task.taskdate < weeklater:
        duethisweek = True
        print '\t[%s] %s' % (task.project, task.task)
if not duethisweek:
    print '\t (none)'

print '\nTODO NEXT\n'

for task in flaglist:
    if task.type == 'week':
        week = True
        print '\t[%s] %s' % (task.project, task.task)
if not week:
    print '\t (none)'


'''
print '\nSTARTING THIS WEEK\n'

for task in flaglist:
    weeklater = today_date + timedelta(days=7)
    if task.type == 'start' and today_date < task.taskdate < weeklater:
        startthisweek = True
        print '\t[%s] %s' % (task.project, task.task)
if not startthisweek:
    print '\t (none)'
'''
if len(errlist) != 0:
    print '\nERROR PARSING THESE LINES\n'
    for errtask in errlist:
        print '\t%s' % str(errtask)

print '\n'
