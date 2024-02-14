 """
This script scrapes the DTU course evaluation and grade data from the DTU website and stores it in coursedic.json.
It uses the course numbers from coursenumbers.txt (from getCourseNumbers.py) and the key from the env var SESSION_ID
to access the data.
"""
import time
start_time = time.time()

import requests
import re
import pprint
from bs4 import BeautifulSoup
import json
import datetime
import traceback
from tqdm import tqdm
import os

now = datetime.datetime.now()

pp = pprint.PrettyPrinter(indent=2)

file = open("coursenumbers.txt", 'r')
courses = file.read().split(",")
file.close()

key = os.environ.get('SESSION_ID', False)
if not key:
    BOLD = '\033[1m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

    print(BOLD, WARNING, "No SESSION_ID found in environment variables.")
    print("Add a Github Secrets (see https://docs.github.com/en/actions/security-guides/using-secrets-in-github"
          "-actions#creating-secrets-for-a-repository) named SESSION_ID containing the value of the ASP.NET_SessionId"
          " cookie from kurser.dtu.dk", ENDC)
    exit(-1)


def printlog(txt):
    f = open('out.txt', 'w')
    print(txt)
    f.write(txt + '\n')  # python will convert \n to os.linesep


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
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.findAll('a')
    links = []
    for a in anchors:
        links.append(a['href'])
    return links


reqC = 0


def respObj(url):
    global reqC
    reqC += 1
    r = requests.get(url, cookies={'ASP.NET_SessionId': key})
    if r.status_code == 200:
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


gradeHTMLNames = ["Ej m&#248;dt", "Syg", "Best&#229;et", "Ikke best&#229;et", "-3", "00", "02", "4", "7", "10", "12"]
grades = ["absent", "sick", "p", "np", "-3", "00", "02", "4", "7", "10", "12"]


class Course(object):
    def __init__(self, courseN):
        self.courseN = courseN
        self.initDic()
        self.reviewLinks = []
        self.gradeLinks = []

    def initDic(self):
        self.dic = {}
        for grade in grades:
            self.dic[grade] = 0

    def setHTML(self, HTML):
        self.HTML = HTML
        self.soup = BeautifulSoup(HTML, 'html.parser')

    def extractParticipants(self):

        return self.participants

    def extractGrades(self, url):
        try:
            html = respObj(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                obj = soup.find_all('table')[2].find_all('tr')
                dic = {};
                for i in range(1, len(obj)):
                    name = removeWhitespace(obj[i].find_all('td')[0].text)
                    val = removeWhitespace(obj[i].find_all('td')[1].text)
                    dic[name] = val
                # pp.pprint(dic);
                timestamp = url.split("/")[-1]
                season = timestamp.split("-")[0]
                year = timestamp.split("-")[-1]
                if (int(year) > now.year + 2):
                    year = str(int(year) - 100)
                    timestamp = season + "-" + year
                dic["timestamp"] = timestamp

                participants = int(removeWhitespace(soup.find_all('table')[0].find_all('tr')[1].find_all('td')[1].text))
                dic["participants"] = participants

                pass_percentage = int(removeWhitespace(
                    soup.find_all('table')[0].find_all('tr')[2].findChildren()[1].text.split("(")[1].split("%")[0]))
                dic["pass_percentage"] = pass_percentage

                try:
                    avg = float(removeWhitespace(
                        soup.find_all('table')[0].find_all('tr')[3].findChildren()[1].text.split(" (")[0]).replace(",",
                                                                                                                   "."))
                    dic["avg"] = avg
                except Exception:
                    traceback.format_exc()
                return dic;
            return False;
        except IndexError as e:
            return False

    def extractReviews(self, url):
        # url="https://evaluering.dtu.dk/kursus/01005/122714"

        dic = {}
        try:
            html = respObj(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                containers = soup.findAll("div", {"class": "ResultCourseModelWrapper"})  # [2].find_all('tr')

                publicContainer = soup.find("div", {"id": "CourseResultsPublicContainer"})
                dic["participants"] = int(publicContainer.find("table").findAll("tr")[1].findAll("td")[0].text)
                dic["timestamp"] = publicContainer.find("h2").text[-3:]
                firstOptionLabel = soup.find("div", {"class": "RowWrapper"}).find("div", {
                    "class": "FinalEvaluation_Result_OptionColumn"})
                if firstOptionLabel:
                    dic["firstOption"] = firstOptionLabel.text
                else:
                    print("No sorting found for \"", removeWhitespace(publicContainer.find("h2").text),
                          "\" results may be wrong")
                for container in containers:
                    name = container.find("div", {"class": "FinalEvaluation_Result_QuestionPositionColumn"}).text
                    name = removeWhitespace(name)
                    dic[name] = {}
                    dic[name]["question"] = container.find("div", {"class": "FinalEvaluation_QuestionText"}).text
                    for i, row in enumerate(container.findAll("div", {"class": "RowWrapper"})):
                        dic[name][i] = removeWhitespace(
                            row.find("div", {"class": "FinalEvaluation_Result_AnswerCountColumn"}).find("span").text)
            return dic
        except KeyError:
            return False

    def gather(self):
        dic = {}
        d = [["grades", self.gradeLinks, self.extractGrades], ["reviews", self.reviewLinks, self.extractReviews]]
        foundData = False
        for lst in d:
            crawl = self.crawl(lst[0], lst[1], lst[2])
            if (crawl):
                dic[lst[0]] = crawl
                foundData = True
        if (foundData):
            return dic
        else:
            return False

    def crawl(self, name, URLs, f):
        lst = []
        foundData = False
        for i, link in enumerate(URLs):
            data = f(link)
            if (data):
                foundData = True
                data["url"] = link
                lst.append(data)
        if (foundData):
            return lst
        else:
            return False

    def __str__(self):
        return "Course: %s" % (self.courseN)


courseDic = {}

for i, courseN in tqdm(enumerate(courses), total=len(courses)):
    try:
        # print("Course: "+courseN)
        course = Course(courseN)
        overviewResp = respObj("http://kurser.dtu.dk/course/" + courseN + "/info")

        if overviewResp:
            soup = BeautifulSoup(overviewResp, "html.parser")
            links = soup.find_all('a')
            for link in links:
                l = link.get('href')
                if "evaluering" in l:
                    course.reviewLinks.append(l)
                elif "karakterer" in l:
                    course.gradeLinks.append(l)
        crawl = course.gather()
        if (crawl):
            courseDic[courseN] = crawl
            soup = BeautifulSoup(respObj("http://kurser.dtu.dk/course/" + courseN), "html.parser")
            courseName = soup.find_all('h2')[0].contents[0].split(" ", 1)[1]
            courseDic[courseN]["name"] = courseName
    except KeyboardInterrupt:
        break
    except Exception as e:
        printlog(str(e))
        printlog("Skipping " + str(courseN))

with open('coursedic.json', 'w') as outfile:
    json.dump(courseDic, outfile)
    outfile.close()

printlog("Requests sent: " + str(reqC))
