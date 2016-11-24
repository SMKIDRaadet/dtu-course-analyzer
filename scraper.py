import urllib2
import re
import pickle
import pprint
from bs4 import BeautifulSoup
grades=["Ej m&#248;dt", "Syg", "-3", "00", "02", "4", "7", "10", "12"]
bachelor_courses=["01005", "01006", "01015", "01016", "01017", "01025", "01035", "01037", "01125", "01237", "01666", "02101", "02102", "02105", "02121", "02122", "02128", "02131", "02138", "02139", "02141", "02148", "02155", "02156", "02157", "02158", "02159", "02161", "02170", "02190", "02350", "02402", "02403", "02405", "02413", "02450", "02502", "02511", "02512", "02525", "02526", "02601", "02602", "02609", "02631", "02632", "02633", "02634", "10018", "10020", "10022", "10024", "10031", "10033", "10034", "10036", "10041", "10044", "10050", "10052", "10054", "10102", "10103", "10104", "10209", "10240", "10303", "10347", "10420", "10467", "10720", "10721", "10722", "10811", "10900", "11000", "11010", "11031", "11110", "11112", "11121", "11140", "11141", "11203", "11305", "11311", "11318", "11341", "11342", "11343", "11411", "11450", "11462", "11463", "11525", "11561", "11562", "11691", "11990", "11993", "11994", "11995", "11996", "11997", "12000", "12003", "12102", "12134", "12139", "12143", "12202", "12203", "12205", "12210", "12320", "12500", "12701", "12810", "12811", "23561", "23711", "23732", "23733", "23734", "24001", "24002", "24004", "24005", "24007", "25102", "25104", "25105", "26000", "26003", "26006", "26008", "26009", "26010", "26011", "26027", "26028", "26030", "26050", "26122", "26124", "26125", "26199", "26201", "26202", "26222", "26225", "26245", "26261", "26299", "26301", "26400", "26407", "26411", "26426", "26428", "26499", "27002", "27004", "27007", "27008", "27015", "27016", "27022", "27023", "27026", "27027", "27034", "27035", "27040", "27042", "27051", "27461", "27611", "27633", "28001", "28020", "28025", "28121", "28122", "28123", "28124", "28125", "28140", "28150", "28160", "28221", "30010", "30020", "30100", "30110", "30120", "30130", "30140", "30150", "30160", "31001", "31003", "31013", "31015", "31300", "31342", "31343", "31344", "31345", "31351", "31373", "31400", "31405", "31501", "31502", "31511", "31520", "31522", "31533", "31534", "31540", "31561", "31605", "31606", "31631", "31700", "31932", "31933", "33236", "33253", "33255", "33257", "33323", "33470", "33471", "33472", "33480", "33481", "33482", "34020", "34021", "34029", "34031", "34120", "34126", "34127", "34129", "34210", "34220", "34229", "34302", "34311", "34315", "34318", "34319", "34330", "41000", "41010", "41012", "41015", "41020", "41030", "41031", "41035", "41045", "41051", "41102", "41112", "41202", "41203", "41263", "41271", "41280", "41312", "41342", "41344", "41401", "41402", "41409", "41422", "41501", "41502", "41511", "41560", "41603", "41612", "41616", "41617", "41618", "41650", "41651", "41659", "41680", "41704", "41706", "41713", "41801", "41812", "41814", "41842", "42005", "42011", "42021", "42042", "42062", "42101", "42107", "42175", "42176", "42270", "42340", "42352", "42406", "42415", "42421", "42429", "42430", "42554", "42580", "42582", "42583", "42584", "42585", "42610", "42872", "42873", "42874", "42875", "42876", "46000", "46010", "46440", "47321", "47421", "KU002", "KU003", "KU004", "KU005", "KU006", "KU009", "KU010", "KU011", "KU012"]
key='ASP.NET_SessionId=oukrstjkbnd21jccxstgmbdz'


#printlog content

#f = open('myfile.txt','w')
#f.write(content) # python will convert \n to os.linesep
#f.close() # you can omit in most cases as the destructor will call it
f = open('out.txt','w')
def printlog(txt):
    print(txt)
    f.write(txt+'\n') # python will convert \n to os.linesep

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
def gethtml(url):
    req = urllib2.Request(url)
    req.add_header('Cookie', key)
    resp = urllib2.urlopen(req)
    return resp


gradesDB=[]
reviewsDB=[]
grades_success_counter=0
reviews_success_counter=0
for i, course in enumerate(bachelor_courses):
    printlog("Analyzing course:" + course)
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
            resp = gethtml(review)
            if resp.getcode()==200:
                content = resp.read()
                content = " ".join(content.split())
                lst= content.split('FinalEvaluation_Result_AnswerCountColumn">')
                lst.pop(0)

                if len(lst) == 43:
                    reviewsDB.append([])
                    reviewsDB[reviews_success_counter].append(str(course))
                    for ls in lst:
                        reviewval=int(extractstr('', '<', ls))
                        reviewsDB[reviews_success_counter].append(int( reviewval ))  
                    reviews_success_counter+=1
                    break
                else:
                    printlog("Error: Unexpected length of review value list")
    else:
        printlog("Error formatting review overview")

    exams=extractURLs('Karakterhistorik', '/a> </div> </div> </div>', infostr);
    if exams != "":
        for exam in exams:
            printlog(exam)
            if (exam != ''):
                printlog("Exam found: " + exam)
                resp = gethtml(exam)
                if resp.getcode()==200:
                    content = resp.read()
                    content = " ".join(content.split())
                    content = content.split('Fremm&#248;dte </td> <td', 1)[1]
                    found = extractstr('> ', ' </td>', content)
                    if (found != ''):
                        printlog("Participants:" + found)
                        participants=int(found);
                        if participants >= 5:
                            printlog("Enough participants")
                            grades_given = []
                            error=0

                            tmpgradeslist=[]
                            for grade in grades:
                                nppl = extractstr(grade + ' </td> <td style="text-align: center"> ', ' </td> <td style="vertical-align', content)
                                if (nppl == ''):
                                    nppl=0
                                    if ( (grade==grades[0]) or (grade==grades[1]) ):
                                        printlog("Warning: No entry for " + grade)
                                    else:

                                        printlog("Error: No entry for " + grade)
                                        error=1
                                printlog(grade+": " + str(nppl))
                                tmpgradeslist.append(int(nppl))
                            if error==0:
                                gradesDB.append([])
                                gradesDB[grades_success_counter].append(str(course))
                                gradesDB[grades_success_counter].append(participants)
                                gradesDB[grades_success_counter].extend(tmpgradeslist)
                                printlog("Breaking")
                                grades_success_counter+=1
                                break
                        else:
                            printlog("Not enough participants")
            else:
                printlog("Error with exam: " + exam)
    else:
        printlog("Error formatting exam overview")
    printlog("")  

f = open('gradesDB.txt', 'wb')
pickle.dump(gradesDB, f)
f.close()

f = open('reviewsDB.txt', 'wb')
pickle.dump(reviewsDB, f)
f.close()

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(gradesDB)
pp.pprint(reviewsDB)