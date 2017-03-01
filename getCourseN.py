# -*- coding: utf8 -*-
import json
import time
start_time = time.time()

import requests
import re
import pickle
import pprint
from bs4 import BeautifulSoup#
import json
import sys
import datetime
import traceback

now = datetime.datetime.now()

pp = pprint.PrettyPrinter(indent=2)

file = open("coursenumbers.txt", 'r')
courses=file.read().split(",")
file.close()

file = open("secret.txt", 'r')
key=file.read()
file.close()


with open('coursedic.json') as file:
    courseDic = json.load(file)


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
    except Exception:
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
    reqC += 1
    r = requests.get(url, cookies={'ASP.NET_SessionId' : key})
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
    txt = txt.replace(" ", "")
    return txt

gradeHTMLNames=["Ej m&#248;dt", "Syg", "Best&#229;et", "Ikke best&#229;et", "-3", "00", "02", "4", "7", "10", "12"]
grades=["absent", "sick", "p", "np", "-3", "00", "02", "4", "7", "10", "12"]

class Course(object):
    def __init__(self, courseN):
        self.courseN = courseN
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

        return self.participants

    def extractGrades(self, url):
        try:
            html = respObj(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                obj = soup.find_all('table')[2].find_all('tr')
                dic={};
                for i in range(1, len(obj)):
                    name = removeWhitespace( obj[i].find_all('td')[0].text )
                    val = removeWhitespace( obj[i].find_all('td')[1].text )
                    dic[name]=val
                #pp.pprint(dic);
                timestamp = url.split("/")[-1]
                season = timestamp.split("-")[0]
                year = timestamp.split("-")[-1]
                if( int(year) > now.year+2):
                    year = str(int(year)-100)
                    timestamp=season + "-" + year
                dic["timestamp"] = timestamp

                participants = int(removeWhitespace(soup.find_all('table')[0].find_all('tr')[1].find_all('td')[1].text))
                dic["participants"] = participants

                pass_percentage = int(removeWhitespace(soup.find_all('table')[0].find_all('tr')[2].findChildren()[1].text.split("(")[1].split("%")[0]))
                dic["pass_percentage"] = pass_percentage

                try:
                    avg = float(removeWhitespace(soup.find_all('table')[0].find_all('tr')[3].findChildren()[1].text.split(" (")[0]).replace(",", "."))
                    dic["avg"] = avg
                except Exception:
                    traceback.format_exc()
                return dic;
            return False;
        except IndexError as e:
            return False

    def extractReviews(self, url):
        #url="https://evaluering.dtu.dk/kursus/01005/122714"

        dic = {}
        try:
            html = respObj(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                obj = soup.find_all('table')[2].find_all('tr')

                participants = int(soup.findAll("td", { "class" : "FinalEvaluation_Result_QuestionPositionColumn" })[1].text)
                dic["participants"]=participants
                for i in range(1, len(obj)):
                    if (obj[i]["class"][0] == 'context_subheader'):
                        qCounter = 0
                        name = removeWhitespace(obj[i].find_all('td')[0].text)
                        question = (obj[i].find_all('td')[1].findChildren()[0].text)
                        dic[name] = {}
                        dic[name]["question"] = question
                    else:
                        value = removeWhitespace(obj[i].find_all('td')[2].text)
                        dic[name][qCounter] = value
                        qCounter += 1

            return dic
        except KeyError:
            return False

    def gather(self):
        dic = {}
        d = [["grades", self.gradeLinks, self.extractGrades], ["reviews", self.reviewLinks, self.extractReviews]]
        foundData = False
        for lst in d:
            crawl = self.crawl(lst[0], lst[1], lst[2])
            if(crawl):
                dic[lst[0]] = crawl
                foundData = True
        if(foundData):
            return dic
        else:
            return False


    def crawl(self, name, URLs, f):
        lst = []
        foundData = False
        for i, link in enumerate(URLs):
            data = f(link)
            if(data):
                foundData = True
                data["url"] = link
                lst.append(data)
        if(foundData):
            return lst
        else:
            return False

    def __str__(self):
        return "Course: %s" % (self.courseN)


for i, courseN in enumerate(courses):
    try:
        print("Course: "+courseN)
        course = Course(courseN)
        overviewResp = respObj("http://kurser.dtu.dk/course/" + courseN)
        if overviewResp:
            soup = BeautifulSoup(overviewResp, "html.parser")
            h2 = soup.find_all('h2')[0]
            courseName = h2.contents[0].split(" ", 1)[1]
            print(courseName)
            courseDic[courseN]["name"] = courseName
    except Exception:
        printlog("Skipping " + str(courseN))

with open('coursedic_with_courseN.json', 'w') as outfile:
    json.dump(courseDic, outfile)
    outfile.close()

pp.pprint(courseDic['01236'])

printlog("Requests sent: " + str(reqC))