import urllib2
import re
grades=["Ej m&#248;dt", "Syg", "-3", "00", "02", "4", "7", "10", "12"]
bachelor_courses=["26027", "01005", "01006", "01015", "01016", "01017", "01025", "01035", "01037", "01125", "01237", "01666", "02101", "02102", "02105", "02121", "02122", "02128", "02131", "02138", "02139", "02141", "02148", "02155", "02156", "02157", "02158", "02159", "02161", "02170", "02190", "02350", "02402", "02403", "02405", "02413", "02450", "02502", "02511", "02512", "02525", "02526", "02601", "02602", "02609", "02631", "02632", "02633", "02634", "10018", "10020", "10022", "10024", "10031", "10033", "10034", "10036", "10041", "10044", "10050", "10052", "10054", "10102", "10103", "10104", "10209", "10240", "10303", "10347", "10420", "10467", "10720", "10721", "10722", "10811", "10900", "11000", "11010", "11031", "11110", "11112", "11121", "11140", "11141", "11203", "11305", "11311", "11318", "11341", "11342", "11343", "11411", "11450", "11462", "11463", "11525", "11561", "11562", "11691", "11990", "11993", "11994", "11995", "11996", "11997", "12000", "12003", "12102", "12134", "12139", "12143", "12202", "12203", "12205", "12210", "12320", "12500", "12701", "12810", "12811", "23561", "23711", "23732", "23733", "23734", "24001", "24002", "24004", "24005", "24007", "25102", "25104", "25105", "26000", "26003", "26006", "26008", "26009", "26010", "26011", "26027", "26028", "26030", "26050", "26122", "26124", "26125", "26199", "26201", "26202", "26222", "26225", "26245", "26261", "26299", "26301", "26400", "26407", "26411", "26426", "26428", "26499", "27002", "27004", "27007", "27008", "27015", "27016", "27022", "27023", "27026", "27027", "27034", "27035", "27040", "27042", "27051", "27461", "27611", "27633", "28001", "28020", "28025", "28121", "28122", "28123", "28124", "28125", "28140", "28150", "28160", "28221", "30010", "30020", "30100", "30110", "30120", "30130", "30140", "30150", "30160", "31001", "31003", "31013", "31015", "31300", "31342", "31343", "31344", "31345", "31351", "31373", "31400", "31405", "31501", "31502", "31511", "31520", "31522", "31533", "31534", "31540", "31561", "31605", "31606", "31631", "31700", "31932", "31933", "33236", "33253", "33255", "33257", "33323", "33470", "33471", "33472", "33480", "33481", "33482", "34020", "34021", "34029", "34031", "34120", "34126", "34127", "34129", "34210", "34220", "34229", "34302", "34311", "34315", "34318", "34319", "34330", "41000", "41010", "41012", "41015", "41020", "41030", "41031", "41035", "41045", "41051", "41102", "41112", "41202", "41203", "41263", "41271", "41280", "41312", "41342", "41344", "41401", "41402", "41409", "41422", "41501", "41502", "41511", "41560", "41603", "41612", "41616", "41617", "41618", "41650", "41651", "41659", "41680", "41704", "41706", "41713", "41801", "41812", "41814", "41842", "42005", "42011", "42021", "42042", "42062", "42101", "42107", "42175", "42176", "42270", "42340", "42352", "42406", "42415", "42421", "42429", "42430", "42554", "42580", "42582", "42583", "42584", "42585", "42610", "42872", "42873", "42874", "42875", "42876", "46000", "46010", "46440", "47321", "47421", "KU002", "KU003", "KU004", "KU005", "KU006", "KU009", "KU010", "KU011", "KU012"]
key='ASP.NET_SessionId=***REMOVED***'


#print content

#f = open('myfile.txt','w')
#f.write(content) # python will convert \n to os.linesep
#f.close() # you can omit in most cases as the destructor will call it


gradesDB=[]

for i, course in enumerate(bachelor_courses):
    print "Analyzing course:" + course
    gradesDB.append([])
    #http://karakterer.dtu.dk/Histogram/1/26027/Summer-2016
    #req = urllib2.Request('http://karakterer.dtu.dk/Histogram/1/'+course+'/Summer-2016')
    req = urllib2.Request('http://kurser.dtu.dk/course/' + course + '/info')
    req.add_header('Cookie', key)
    resp = urllib2.urlopen(req)


    try:
        grade_overview = " ".join(resp.read().split())
        grade_overview = grade_overview.split('Karakterhistorik', 1)[1]
        grade_overview = grade_overview.split('/a> </div> </div> </div>', 1)[0]
        exams=[]
        exams= grade_overview.split('href')
    except:
        print "Error formatting exam overview"
        continue

    exams.pop(0)
    for exam in exams:
        m = re.search('="(.+?)">', exam)
        if m:
            examurl = m.group(1)
            print "Exam found: " + examurl
            req = urllib2.Request(examurl)
            req.add_header('Cookie', key)
            resp = urllib2.urlopen(req)
            if resp.getcode()==200:
                content = resp.read()
                content = " ".join(content.split())
                #print content
                m = re.search('Fremm&#248;dte </td> <td> (.+?) </td>', content)
                if m:
                    found = m.group(1)
                    print "Participants:" + found
                    participants=int(found);
                    if participants >= 5:
                        print "Enough participants"
                        grades_given = []
                        error=0
                        for j, grade in enumerate(grades):
                            m = re.search(grade + ' </td> <td style="text-align: center"> (.+?) </td> <td style="vertical-align', content)
                            if m:
                                nppl = m.group(1)
                                print grade+": " + str(nppl)
                                #grades_given.append(int(nppl))
                                gradesDB[i].append(int(nppl))
                            else:
                                print "Error finding entry for " + grade
                                if grade!=grades[0] || grades!=grades[1]:
                                    error=1
                        if error==0:
                            print "Breaking"
                            break
                    else:
                        print "Not enough participants"
        else:
            print "Error with exam: " + exam
    

##    if resp.getcode()==200:
##        content = resp.read()
##        content = " ".join(content.split())
##        m = re.search('Fremm&#248;dte </td> <td> (.+?) </td>', content)
##        if m:
##            found = m.group(1)
##            print "Participants:" + found
##
##            participants=int(found);
##
##            if participants >= 5:
##                print "Enough participants"
##                grades_given = []
##                for j, grade in enumerate(grades):
##                    m = re.search(grade + ' </td> <td style="text-align: center"> (.+?) </td> <td style="vertical-align', content)
##                    if m:
##                        nppl = m.group(1)
##                        print grade+": " + str(nppl)
##                        #grades_given.append(int(nppl))
##                        gradesDB[i].append(int(nppl))
##                    else:
##                        print "Error finding entry for " + grade
##            else:
##                print "Not enough participants"
##        else:
##            print "Error: participants entry not found!"
##    else:
##        print "Wrong response code: " + str(resp.getcode())


