"""
This file analyse the data from coursedic.json and create the result in the data.json, [extension]/db.html
and [extension]/db/data.js.
"""

import json
import sys
import pprint
from Prepender import *

if len(sys.argv) != 2:
    print('usage: ' + sys.argv[0] + ' <extension-folder-name>')
    sys.exit()

pp = pprint.PrettyPrinter(indent=2)

with open('coursedic.json') as file:
    courseDic = json.load(file)

db = {}
grades = ["-3", "00", "02", "4", "7", "10", "12"]

pass_percentages = []
workloads = []
qualityscores = []
avg = []

def calcScore(dic, bestOptionFirst):
    score = 0
    total_votes = 0

    for id, votes in dic.items():
        if id != "question":
            if bestOptionFirst: 
                score += (5 - int(id)) * int(votes)
            else:
                score += (1 + int(id)) * int(votes)
            total_votes += int(votes)
    return score / total_votes


for courseN, course in courseDic.items():
    print("Course: " + courseN)
    db[courseN] = {}
    db_sheet = db[courseN]
    for categoryN, sheets in course.items():

        if categoryN == "name":
            db_sheet["name"] = sheets
            continue
        sheet = sheets[0]
        if (len(sheets) >= 2):
            if (sheets[1]["participants"] > sheets[0]["participants"] * 2 or sheets[0]["participants"] < 5):
                sheet = sheets[1]

        if (sheet["participants"] < 5):
            continue

        if categoryN == "grades":
            # pp.pprint(category)
            db_sheet["passpercent"] = sheet["pass_percentage"]
            try:
                db_sheet["avg"] = sheet["avg"]
                avg.append([courseN, sheet["avg"]])
            except Exception:
                pass
            # print(sheet["pass_percentage"])
            pass_percentages.append([courseN, sheet["pass_percentage"]])

            db_sheet["grades"] = {}
            try:
                for grade in grades:
                    db_sheet["grades"][grade] = sheet[grade]
                # print(grade,sheet[grade])
            except Exception:
                pass

        if categoryN == "reviews":
            bestOptionFirst = None
            if sheet["firstOption"] == "Helt uenig":
                bestOptionFirst = False
            elif sheet["firstOption"] == "Helt enig":
                bestOptionFirst = True
            try:
                workloads.append([courseN, calcScore(sheet["2.1"], True)])
                qualityscores.append([courseN, calcScore(sheet["1.1"], bestOptionFirst)])
            except Exception as e:
                #print("Error in calculating scores:", str(e))            
                pass

def insertPercentile(lst, tag):
    global db
    lst.sort(key=lambda sublist: sublist[0], reverse=True)
    lst.sort(key=lambda sublist: sublist[1])

    prev_val = -1
    index = -1
    for i, course in enumerate(lst):
        val = course[1]
        if val > prev_val:
            index += 1
        course.append(index)

        prev_val = val
    # pass_percentages[1][2] = 1337

    for i, course in enumerate(lst):
        course.append(round(100 * course[2] / (index), 1))
        db[course[0]][tag] = course[3]
    return lst


# pp.pprint(db)
insertPercentile(pass_percentages, "pp")
insertPercentile(avg, "avgp")
insertPercentile(qualityscores, "qualityscore")
insertPercentile(workloads, "workload")

lazyscores = []
for courseN, course in db.items():
    try:
        lazyscores.append([courseN, course['pp'] + course['workload']])
    except Exception:
        pass

# pp.pprint(lazyscores)

insertPercentile(lazyscores, "lazyscore")

# print("a:"+str(pass_percentages[1][1]))

empty_keys = [k for k, v in db.items() if not v]
for k in empty_keys:
    del db[k]

folder = sys.argv[1]
extFilename = folder + '/db/data.js'
with open(extFilename, 'w') as outfile:
    json.dump(db, outfile)

with PrependToFile(extFilename) as f:
    f.write_line('var data = ')

with open('data.json', 'w') as outfile:
    json.dump(db, outfile)

table = ''
headNames = [["name", "Name"], ["avg", "Average Grade"], ["avgp", "Average Grade Percentile"], ["passpercent", "Percent Passed"],
             ["qualityscore", "Course Rating"], ["workload", "Workload"], ["lazyscore", "Lazy Score Percentile"]]
table += '<table id="example" class="display" cellspacing="0" width="100%"><thead><tr>'
table += '<th>Course</th>'
for header in headNames:
    table += '<th>' + header[1] + '</th>'
table += '</tr></thead><tbody>'

for course, data in db.items():
    table += '<tr>'
    table += '<td>' + '<a href="http://kurser.dtu.dk/course/' + course + '">' + course + '</a></td>'
    for header in headNames:
        key = header[0]
        val = ""
        if key in data:
            val = str(data[key])

        table += '<td>' + val + '</td>'
    table += '</tr>'
table += '</tbody></table>'


file = open("templates/db.html", 'r')
content=file.read()
file.close()

content = content.replace('$table', table)

file = open(folder + "/db.html", 'w')
content=file.write(content)
file.close()

file = open("templates/init_table.js", 'r')
content=file.read()
file.close()

searchable_columns = '{ "bSearchable": true, "aTargets": [ 0 ] }'
for i in range(0, len(headNames)):
    if i > 0:
        sort_str = '"asSorting": [ "desc", "asc" ], "bSearchable": false, '
    else:
        sort_str = '"bSearchable": true,'
    searchable_columns += ', { type: "non-empty", ' + sort_str + '"aTargets": [ ' + str(i+1) + ' ] }'

content = content.replace('$searchable_columns', searchable_columns)

file = open(folder + "/js/init_table.js", 'w')
content=file.write(content)
file.close()