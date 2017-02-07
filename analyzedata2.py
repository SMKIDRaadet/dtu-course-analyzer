import json
import sys
import pprint

pp = pprint.PrettyPrinter(indent=2)


with open('coursedic.json') as file:
    courseDic = json.load(file)

db = {}
grades = ["-3", "00", "02", "4", "7", "10", "12"]

pass_percentages = []
for courseN, course in courseDic.items():
    print("Course: "+courseN)
    db[courseN]={}
    for categoryN, sheets in course.items():
        if categoryN == "grades":
            #pp.pprint(category)
            sheet = sheets[0]
            try:
                if(sheets[1]["participants"] > sheets[0]["participants"]*2):
                    sheet = sheets[1]
            except Exception:
                pass


            db[courseN]["passpercent"] = sheet["pass_percentage"]
            try:
                db[courseN]["avg"] = sheet["avg"]
            except Exception:
                pass
            #print(sheet["pass_percentage"])
            pass_percentages.append([courseN, sheet["pass_percentage"]])

            db[courseN]["grades"] = {}
            try:
                for grade in grades:
                    db[courseN]["grades"][grade] = sheet[grade]
                    print(grade,sheet[grade])
            except Exception:
                pass
            #for exam, grades in category.items():

                #print(grades)
                #print(grades['pass_percentage'])
                #
                #print("--------------------------------------------------------------------------")
                #for a in exam.items():
                 #   print(a)
pass_percentages.sort(key=lambda sublist: sublist[0], reverse=True)
pass_percentages.sort(key=lambda sublist: sublist[1])

prev_val = -1
index=0
for i, lst in enumerate(pass_percentages):
    val = lst[1]
    lst.append(index)
    if val > prev_val:
        index+=1
    prev_val = val
    #pass_percentages[1][2] = 1337

for i, lst in enumerate(pass_percentages):
    lst.append(round(100 * lst[2] / (index-1), 1))
#pp.pprint(db)
pp.pprint(pass_percentages)
print("a:"+str(pass_percentages[1][1]))
