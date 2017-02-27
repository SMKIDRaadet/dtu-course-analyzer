import json
import sys
import pprint

pp = pprint.PrettyPrinter(indent=2)


with open('coursedic.json') as file:
    courseDic = json.load(file)

db = {}
grades = ["-3", "00", "02", "4", "7", "10", "12"]

pass_percentages = []
workloads = []
qualityscores = []
avg = []

def calcScore(dic):
    score = 0
    total_votes = 0
    for id, votes in dic.items():
        if id != "question":
            score += (int(id)) * int(votes)
            total_votes += int(votes)
    return score / total_votes

for courseN, course in courseDic.items():
    print("Course: "+courseN)
    db[courseN]={}
    db_sheet = db[courseN]
    for categoryN, sheets in course.items():

        sheet = sheets[0]
        if (len(sheets) >= 2):
            if (sheets[1]["participants"] > sheets[0]["participants"] * 2 or sheets[0]["participants"] < 5):
                sheet = sheets[1]

        if (sheet["participants"] < 5):
            continue

        if categoryN == "grades":
            #pp.pprint(category)
            db_sheet["passpercent"] = sheet["pass_percentage"]
            try:
                db_sheet["avg"] = sheet["avg"]
                avg.append([courseN, sheet["avg"]])
            except Exception:
                pass
            #print(sheet["pass_percentage"])
            pass_percentages.append([courseN, sheet["pass_percentage"]])

            db_sheet["grades"] = {}
            try:
                for grade in grades:
                    db_sheet["grades"][grade] = sheet[grade]
                    #print(grade,sheet[grade])
            except Exception:
                pass

        if categoryN == "reviews":
            workloads.append([courseN, calcScore(sheet["1.6"])])
            qualityscores.append([courseN, calcScore(sheet["1.8"])])

def insertPercentile(lst, tag):
    global db
    lst.sort(key=lambda sublist: sublist[0], reverse=True)
    lst.sort(key=lambda sublist: sublist[1])

    prev_val = -1
    index=-1
    for i, course in enumerate(lst):
        val = course[1]
        if val > prev_val:
            index+=1
        course.append(index)

        prev_val = val
        #pass_percentages[1][2] = 1337

    for i, course in enumerate(lst):
        course.append(round(100 * course[2] / (index), 1))
        db[course[0]][tag]=course[3]
    return lst
#pp.pprint(db)
insertPercentile(pass_percentages, "pp")
insertPercentile(avg, "avgp")
insertPercentile(qualityscores, "qualityscore")
insertPercentile(workloads, "workload")




lazyscores = []
for courseN, course in db.items():
    try:
        lazyscores.append([ courseN, course['pp'] + 100 - course['workload'] ])
    except Exception:
        pass

#pp.pprint(lazyscores)

insertPercentile(lazyscores, "lazyscore")

#print("a:"+str(pass_percentages[1][1]))

pp.pprint(db)