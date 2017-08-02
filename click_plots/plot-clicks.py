#!/usr/bin/python

from matplotlib import pyplot as plt
from matplotlib import dates
from datetime import datetime
import sys

d = []
t = []
for line in sys.stdin:
  dstamp, temp = line.rstrip().split('\t')
  d.append(datetime.strptime(dstamp, '%Y-%m-%d-%H-%M'))
  t.append(int(temp))

days = dates.DayLocator()
hours = dates.HourLocator(interval=3)
dfmt = dates.DateFormatter('              %b %d')

datemin = datetime(2015, 1, 4, 0, 0)
datemax = datetime(2015, 1, 11, 23, 59, 59)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(dfmt)
ax.xaxis.set_minor_locator(hours)
ax.set_xlim(datemin, datemax)
ax.set_ylabel('Temperature (F)')
ax.grid(True)
ax.plot(d, t, linewidth=2)
fig.set_size_inches(8, 4)

plt.savefig('temperatures.pdf', format='pdf')
