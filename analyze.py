import os
import csv
from enum import Enum

class Column(Enum):
    timestamp = 0
    location = 1
    classtime = 2
    open_seats = 3
    taken_seats = 4
    is_full = 5

IS_FULL = 'is_full'
TOTAL_SLOTS = 'total_slots'

summary = {}
with open(os.getcwd() + '/classes.csv', 'r') as csvfile:
    for row in reversed(list(csv.reader(csvfile))):
        if not row: continue
        location_summary = summary.setdefault(row[Column.location.value], {})
        class_summary = location_summary.get(row[Column.classtime.value])

        if not class_summary:
            # this is the last time we checked this class, record if it filled up
            location_summary.setdefault(row[Column.classtime.value], {IS_FULL: row[Column.is_full.value]})
        elif not class_summary.get(TOTAL_SLOTS) and row[Column.open_seats.value]:
            # this check was made when the class wasn't full yet, record total slots
            class_summary[TOTAL_SLOTS] = str(int(row[Column.open_seats.value]) + int(row[Column.taken_seats.value]))
            location_summary.setdefault(row[Column.classtime.value], class_summary)

for location in summary.keys():
    print(location + ":")
    for classtime in summary.get(location).keys():
        print("\tclass at " + classtime +
            " had " + summary.get(location).get(classtime).setdefault(TOTAL_SLOTS, "NA") + " slots" +
            " and was full? " + summary.get(location).get(classtime).setdefault(IS_FULL, "NA"))
