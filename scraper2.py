# -*- coding: utf8 -*-
import time
start_time = time.time()

import urllib3
import requests
import re
import pickle
import pprint
from bs4 import BeautifulSoup#
import json
import sys
import sys

pp = pprint.PrettyPrinter(indent=4)

file = open("coursenumbers.txt", 'r')
courses=file.read().split(",")
file.close()

file = open("secret.txt", 'r')
key=file.read()
file.close()

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
def respObj(url):
    global reqC
    swag={}
    swag['ASP.NET_SessionId']=key
    cookies = swag
    r = requests.get(url, cookies=cookies)
    if r.status_code==200:
        return r.text
    else:
        return False
respObj("http://karakterer.dtu.dk/Histogram/1/02110/Winter-2016")



def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def gradeParticipants(html):
    soup = BeautifulSoup(html, 'html.parser')
    return int(removeWhitespace(soup.find_all('table')[0].find_all('tr')[1].find_all('td')[1].text))
    
def removeWhitespace(txt):
    txt = " ".join(txt.split())
    return txt

gradeHTMLNames=["Ej m&#248;dt", "Syg", "Best&#229;et", "Ikke best&#229;et", "-3", "00", "02", "4", "7", "10", "12"]
grades=["absent", "sick", "p", "np", "-3", "00", "02", "4", "7", "10", "12"]

class Course(object):
    def __init__(self, courseN):
        self.courseN = courseN
        self.participants = 0
        self.initDic()
        self.reviewLinks = []
        self.gradeLinks = []

    def initDic(self):
        self.dic= {}
        for grade in grades:
            self.dic[grade] = 0

    def setHTML(self, HTML):
        self.HTML=HTML
        self.soup=BeautifulSoup(HTML, 'html.parser')

    def extractParticipants(self):
        self.participants = int(removeWhitespace(self.soup.find_all('table')[0].find_all('tr')[1].find_all('td')[1].text))
        return self.participants

    def extractGrades(self, url):
        html = respObj(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            obj = soup.find_all('table')[1].find_all('tr')
            dic={};
            for i in range(2, len(obj)):
                obj = soup.find_all('table')[1].find_all('tr')[i]
                name = removeWhitespace( obj.find_all('td')[0].text )
                val = removeWhitespace( obj.find_all('td')[1].text )
                dic[name]=val
            pp.pprint(dic);
            return dic;
        return False;

    def crawl(self):
        # for i, link in enumerate(links):
        #     gradeResp0 = respObj(link)
        #     print("Finding participants for " + link)
        #     if gradeResp0[0] == 200:
        #         participants0 = gradeParticipants(gradeResp0[1])
        #         print("Participants: " + str(participants0))
        #         if participants0 == 5:
        #             print("Checking if next has twice as many parts.")
        #             gradeResp1 = respObj(gradeLinks[i + 1])
        #             if gradeResp1[0] == 200:
        #                 participants1 = gradeParticipants(gradeResp1[1])
        #                 print("Participants+1: " + str(participants1))
        #                 if float(participants1) * 2 > float(participants0):
        #                     print("Returning resp1")
        #                     return gradeResp1
        #                 else:
        #                     print("Returning resp0")
        #                     return gradeResp0
        for i, link in enumerate(self.gradeLinks):
            self.extractGrades(link);

    def __str__(self):
        return "Course: %s" % (self.courseN)

# c=Course("01018")
# txt=respObj("http://karakterer.dtu.dk/Histogram/1/01005-3/Summer-2016")
# c.setHTML(txt)
# print(str(c.extractParticipants()))
# c.extractGrades()
#

for i, courseN in enumerate(courses[0:5]):
    course = Course(courseN)
    overviewResp = respObj("http://kurser.dtu.dk/course/" + courseN + "/info")
    if overviewResp:
        soup = BeautifulSoup(overviewResp, "html.parser")
        links = soup.find_all('a')
        for link in links:
            l=link.get('href')
            print("Analyzing " + l)
            if "evaluering" in l:
                print("Appending to reviews")
                course.reviewLinks.append(l)
            elif "karakterer" in l:
                print("Appending to grades")
                course.gradeLinks.append(l)
            else:
                printlog("Unknown link, ignoring")
    course.crawl()





f = open('courseDic.txt', 'wb')
#pickle.dump(courseDic, f)
f.close()


#pp.pprint(courseDic)

#printlog("Requests sent: " + str(reqC))