import time
start_time = time.time()

import urllib2
import re
import pickle
import pprint
from bs4 import BeautifulSoup
import json
import sys
import secret

grades=["Ej m&#248;dt", "Syg", "Best&#229;et", "Ikke best&#229;et", "-3", "00", "02", "4", "7", "10", "12"]
gradesfields=list(grades)
gradesfields[0:4]=["dns", "sick", "p", "np"]

# Read all course numbers from file. 
file = open("coursenumbers.txt", 'r')
courses=file.read().split(",")

key='ASP.NET_SessionId=' + secret.sessionID
print 'key=' + key
#printlog content
print courses
#f = open('myfile.txt','w')
#f.write(content) # python will convert \n to os.linesep
#f.close() # you can omit in most cases as the destructor will call it
def printlog(txt):
    f = open('out.txt','w')
    print(txt)
    f.write(txt+'\n') # python will convert \n to os.linesep

def printTime():
    printlog("--- %s seconds ---" % (time.time() - start_time))

def extractstr(pre, post, body):
    m = re.search(pre + '(.+?)' + post, body)
    if m:
        return m.group(1)
    else:
        return ""
def extractURLs(pre, post, body):
    try:
        body = " ".join(body.split())
        body = body.split(pre, 1)[1]
        body = body.split(post, 1)[0]
        return extractlinks(body)
    except:
        return ""

def extractlinks(html):
    soup = BeautifulSoup(html,"html.parser")
    anchors = soup.findAll('a')
    links = []
    for a in anchors:
        links.append(a['href'])
    return links

reqC=0
def gethtml(url):
    global reqC
    reqC+=1
    req = urllib2.Request(url)
    req.add_header('Cookie', key)
    resp = urllib2.urlopen(req)
    return resp
def exp_dict(course):
    global hasExpanded
    if hasExpanded == 0:
        courseDic[course] = {}
    hasExpanded = 1

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False



courseDic={}
fields=["participants", "absent", "sick", "p", "np", "-3", "00", "02", "4", "7", "10", "12"]

for i, course in enumerate(courses):
    printTime()
    courseDic[course] = {}

    hasExpanded=0

    printlog("Analyzing course:" + course + " (" + str(i) + "/" + str(len(courses)) + " : " + str(round( (float(i)/float(len(courses)))*100 ,2)) + "%)")
    #http://karakterer.dtu.dk/Histogram/1/26027/Summer-2016
    #req = urllib2.Request('http://karakterer.dtu.dk/Histogram/1/'+course+'/Summer-2016')
    resp = gethtml('http://kurser.dtu.dk/course/' + course + '/info')

    #<div class="bar">Kursusevalueringer</div>
    infostr = resp.read()
    infostr = " ".join(infostr.split())

    
    reviews=extractURLs('Kursusevalueringer', 'Karakterhistorik', infostr)
    if reviews != "":
        for review in reviews:
            printlog("Review found: " + review)
            try:
                resp = gethtml(review)
                if resp.getcode()==200:
                    content = resp.read()
                    content = " ".join(content.split())
                    content = content.split('FinalEvaluation_Result_QuestionPositionColumn"><b>', 1)[1]
                    participants = int(extractstr('QuestionPositionColumn"><b>', '</b></td><td>har besvaret', content))
                    printlog("Review participants:" + str(participants))
                    if participants >= 5 :
                        lst= content.split('FinalEvaluation_Result_AnswerCountColumn">')
                        lst.pop(0)

                        if len(lst) == 43:
                            courseDic[course]["review"] = {}

                            courseDic[course]["review"]["participants"] = participants
                            for j, ls in enumerate(lst):
                                reviewval=int(extractstr('', '<', ls))
                                courseDic[course]["review"]['A' + str(j)] = int(extractstr('', '<', ls))  
                            break
                        else:
                            printlog("Error: Unexpected length of review value list")
                    else:
                        printlog("Not enough review participants")
            except:
                printlog("Error review")
    else:
        printlog("Warning: Cannot format review overview")

    exams=extractURLs('Karakterhistorik', '/a> </div> </div> </div>', infostr);
    if exams != "":
        for exam in exams:
            printlog(exam)
            if (exam != ''):
                printlog("Exam found: " + exam)
                try:
                    resp = gethtml(exam)
                    if resp.getcode()==200:
                        content = resp.read()
                        content = " ".join(content.split())
                        content = content.split('Fremm&#248;dte </td> <td', 1)[1]
                        found = extractstr('> ', ' </td>', content)
                        if (found != ''):
                            printlog("Exam participants:" + found)
                            participants=int(found);
                            if participants >= 5:
                                #exp_dict(course)
                                #grades_given = []
                                courseDic[course]["grades"] = {}
                                tmpgradeslist=[]

                                for i, grade in enumerate(grades):
                                    nppl = extractstr(grade + ' </td> <td style="text-align: center"> ', ' </td> <td style="vertical-align', content)
                                    if (nppl == ''):
                                        nppl=0
                                        #printlog("Warning: No entry for " + grade)
                                    #print 'courseDic['+str(course)+']["grades"]['+gradesfields[i]+']='+str(nppl)
                                    courseDic[course]["grades"][gradesfields[i]]=int(nppl)
                                    printlog(grade+": " + str(nppl))
                                
                                courseDic[course]["grades"]["participants"] = participants
                                try:
                                    avg = content.join(content.split())
                                    avg = avg.split('Eksamensgennemsnit', 1)[1]
                                    avg = avg.split('Efter 7-',1)[0]
                                    avg = extractstr('<td>',' \(', avg).replace(',', '.')
                                    avg = float(avg)
                                    courseDic[course]["grades"]["avg"] = avg
                                except:
                                    printlog("No avg found")

                                try:
                                    passpercent = content.replace(" ", "")
                                    passpercent = passpercent.split("afdetilmeldte,", 1)[1]
                                    passpercent = float(passpercent.split("%afdefremm", 1)[0].replace(',', '.'))
                                    courseDic[course]["grades"]["passpercent"] = passpercent
                                except:
                                    printlog("No passpercent found")

                                break
                            else:
                                printlog("Not enough exam participants")
                except:
                    printlog("Error exam")
            else:
                printlog("Error with exam: " + exam)
    else:
        printlog("Warning: Cannot format exam overview")
    printlog("")  

f = open('courseDic.txt', 'wb')
pickle.dump(courseDic, f)
f.close()

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(courseDic)

printlog("Requests sent: " + str(reqC))
