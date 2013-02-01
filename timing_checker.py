#!/usr/bin/python
import re, argparse, json, sys, os, mmap, time

time_index = {'time':2,'count':3,'avg':4}


parser = argparse.ArgumentParser(    )
parser.add_argument('timefile',type=argparse.FileType('r'),help='the timefile to process')
parser.add_argument('--top',type=int,default=10,help='Number of items to include in the top list')
parser.add_argument('--sort',choices=time_index.keys(),default='time',help='Sort by')

options = parser.parse_args()

timings = {}

item_line = re.compile("^\s*(.*) Time: (\d*) Count: (\d*) Avg: (\d*)")
header = re.compile("^\S")

items = []

for line in options.timefile:
	result = header.match(line)
	if result:
		current_plugin = line.strip()
	result = item_line.match(line)
	if result:
		eventname = result.group(1)
		items.append( (current_plugin,eventname) + tuple(map(int,result.group(2,3,4))) )



items.sort(key=lambda x:x[time_index.get(options.sort)],reverse=True)

for name, event_type, time, count, avg in items[:options.top]:
	print('{time:15} {avg:10} {count:10} {name} {event_type}'.format(**locals()))