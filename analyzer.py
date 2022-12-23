import json
import sys
import pprint
from Prepender import *
from scipy import stats
from math import sqrt
from collections import namedtuple

if len(sys.argv) != 2:
    print('usage: ' + sys.argv[0] + ' <extension-folder-name>')
    sys.exit()

pp = pprint.PrettyPrinter(indent=2)

with open('coursedic.json') as file:
    courseDic = json.load(file)

data_value = namedtuple('Data_value', ['course', 'value', 'conf_int', 'index'])


db = {}
grades = ["-3", "00", "02", "4", "7", "10", "12"]

pass_percentages = []
workloads = []
qualityscores = []
avg = []

def calcScore(dic):
    # Calculates the average score and the margin of error with a 95% confidence interval using $$t_{0.975} sd/sqrt(n) = t_{0.975} sqrt(var)/sqrt(n) = t_{0.975} sqrt(\sum x_i^n * number_of_times_x=x  / n)/sqrt(n) = t_{0.975} sqrt(\sum x_i^n * number_of_times_x=x )/n$$
    score_sum = 0
    total_votes = 0
    square_sum = 0
    for id, votes in dic.items():
        if id != "question":
            value = 5-int(id)
            score_sum += value * int(votes)
            square_sum += value * value * int(votes)
            total_votes += int(votes)

    avg = score_sum / total_votes
    t = stats.t(df=total_votes-1).ppf(0.975)
    conf_int = t * sqrt(square_sum) / total_votes

    return avg, conf_int


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
                avg.append(data_value(courseN, sheet["avg"], None, None))
            except Exception:
                pass
            # print(sheet["pass_percentage"])
            pass_percentages.append(data_value(courseN, sheet["pass_percentage"], None, None))

            db_sheet["grades"] = {}
            try:
                for grade in grades:
                    db_sheet["grades"][grade] = sheet[grade]
                # print(grade,sheet[grade])
            except Exception:
                pass

        if categoryN == "reviews":
            try:
                two_one = calcScore(sheet["2.1"])
                workloads.append(data_value(courseN, two_one[0], two_one[1], None))
                one_one = calcScore(sheet["1.1"])
                qualityscores.append(data_value(courseN, one_one[0], one_one[1], None))
            except Exception:
                pass


def insertPercentile(lst, tag):
    global db
    lst.sort(key=lambda sublist: sublist.course, reverse=True)
    lst.sort(key=lambda sublist: sublist.value)

    prev_val = -1
    index = -1
    
    indices = {}

    for i, course in enumerate(lst):
        val = course.value
        if val > prev_val:
            index += 1
        indices[course.course] = index

        prev_val = val

    for i, course in enumerate(lst):
        if(indices[course.course]):
            db[course.course][tag] = round(100 *  indices[course.course] / (index), 1)
        if(course.conf_int):
            db[course.course][tag + "_confint"] = "±" + str(course.conf_int)[0:5]
    return lst


# pp.pprint(db)
insertPercentile(pass_percentages, "pp")
insertPercentile(avg, "avgp")
insertPercentile(qualityscores, "qualityscore")
insertPercentile(workloads, "workload")

lazyscores = []
for courseN, course in db.items():
    try:
        lazyscores.append(data_value(courseN, course['pp'] + course['workload'], None))
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
             ["qualityscore", "Course Rating"], ["qualityscore_confint", "Course Rating confidence interval"], ["workload", "Workload"], ["workload_confint", "Workload confidence interval"], ["lazyscore", "Lazy Score Percentile"]]
table += '<table id="example" class="display" cellspacing="0" width="100%"><thead><tr>'
table += '<th>Course</th>'
for header in headNames:
    table += '<th>' + header[1] + '</th>'
table += '</tr></thead>\n<tbody>\n'

for course, data in db.items():
    table += '<tr>'
    table += '<td>' + '<a href="http://kurser.dtu.dk/course/' + course + '">' + course + '</a></td>\n'
    for header in headNames:
        key = header[0]
        val = ""
        if key in data:
            val = str(data[key])

        table += '<td>' + val + '</td>'
    table += '</tr>\n'
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
