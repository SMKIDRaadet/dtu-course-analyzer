import time
import requests
import re
import pprint
from bs4 import BeautifulSoup
import json
import datetime
import traceback
from tqdm import tqdm
import concurrent.futures

# --- CONFIGURATION ---
MAX_WORKERS = 8  # Number of parallel threads. Don't go too high (e.g. >20) to avoid getting blocked.
TIMEOUT = 30     # Seconds to wait for a page before giving up
# ---------------------

start_time = time.time()
now = datetime.datetime.now()
pp = pprint.PrettyPrinter(indent=2)

# Load Course Numbers
try:
    with open("coursenumbers.txt", 'r') as file:
        courses = file.read().split(",")
except FileNotFoundError:
    print("Error: coursenumbers.txt not found.")
    exit(1)

# Load Session Cookie
try:
    with open("secret.txt", 'r') as file:
        key = file.read().strip()
except FileNotFoundError:
    print("Error: secret.txt not found.")
    exit(1)

# Initialize Global Session for Connection Reuse
session = requests.Session()
session.cookies.set('ASP.NET_SessionId', key)
# Headers to look like a real browser
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
})

def printlog(txt):
    # Append to file instead of overwriting every time
    with open('out.txt', 'a') as f:
        # print(txt) # Optional: comment out to reduce console spam
        f.write(txt + '\n')

def extractlinks(html):
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all('a')
    links = []
    for a in anchors:
        if a.has_attr('href'):
            links.append(a['href'])
    return links

def respObj(url):
    try:
        # Use the global session for speed
        r = session.get(url, timeout=TIMEOUT)
        if r.status_code == 200:
            return r.text
    except Exception:
        # Fail silently or log if needed
        pass
    return False

def removeWhitespace(txt):
    return " ".join(txt.split()).replace(" ", "")

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

    def extractGrades(self, url):
        try:
            html = respObj(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                # Use find_all instead of findAll (deprecated)
                tables = soup.find_all('table')
                if len(tables) < 3: return False
                
                obj = tables[2].find_all('tr')
                dic = {}
                for i in range(1, len(obj)):
                    cells = obj[i].find_all('td')
                    if len(cells) >= 2:
                        name = removeWhitespace(cells[0].text)
                        val = removeWhitespace(cells[1].text)
                        dic[name] = val
                
                timestamp = url.split("/")[-1]
                season = timestamp.split("-")[0]
                year = timestamp.split("-")[-1]
                if int(year) > now.year + 2:
                    year = str(int(year) - 100)
                    timestamp = season + "-" + year
                dic["timestamp"] = timestamp

                try:
                    participants = int(removeWhitespace(tables[0].find_all('tr')[1].find_all('td')[1].text))
                    dic["participants"] = participants

                    pass_percentage = int(removeWhitespace(
                        tables[0].find_all('tr')[2].find_all('td')[1].text.split("(")[1].split("%")[0]))
                    dic["pass_percentage"] = pass_percentage

                    avg_text = tables[0].find_all('tr')[3].find_all('td')[1].text.split(" (")[0]
                    dic["avg"] = float(removeWhitespace(avg_text).replace(",", "."))
                except Exception:
                    pass # Data might be missing
                    
                return dic
            return False
        except Exception:
            return False

    def extractReviews(self, url):
        dic = {}
        try:
            html = respObj(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                containers = soup.find_all("div", {"class": "ResultCourseModelWrapper"})
                publicContainer = soup.find("div", {"id": "CourseResultsPublicContainer"})
                
                if not publicContainer: return False

                dic["participants"] = int(publicContainer.find("table").find_all("tr")[1].find_all("td")[0].text)
                dic["timestamp"] = publicContainer.find("h2").text[-3:]
                
                row_wrapper = soup.find("div", {"class": "RowWrapper"})
                if row_wrapper:
                    firstOptionLabel = row_wrapper.find("div", {"class": "FinalEvaluation_Result_OptionColumn"})
                    if firstOptionLabel:
                        dic["firstOption"] = firstOptionLabel.text

                for container in containers:
                    pos_col = container.find("div", {"class": "FinalEvaluation_Result_QuestionPositionColumn"})
                    if not pos_col: continue
                    
                    name = removeWhitespace(pos_col.text)
                    dic[name] = {}
                    q_text = container.find("div", {"class": "FinalEvaluation_QuestionText"})
                    dic[name]["question"] = q_text.text if q_text else ""
                    
                    for i, row in enumerate(container.find_all("div", {"class": "RowWrapper"})):
                        ans_col = row.find("div", {"class": "FinalEvaluation_Result_AnswerCountColumn"})
                        if ans_col:
                            dic[name][i] = removeWhitespace(ans_col.find("span").text)
            return dic
        except Exception:
            return False

    def gather(self):
        dic = {}
        # List of tasks: (name, list_of_links, processing_function)
        tasks = [("grades", self.gradeLinks, self.extractGrades), 
                 ("reviews", self.reviewLinks, self.extractReviews)]
        
        foundData = False
        for name, urls, func in tasks:
            # Helper to process a list of URLs
            lst = []
            for link in urls:
                data = func(link)
                if data:
                    data["url"] = link
                    lst.append(data)
            
            if lst:
                dic[name] = lst
                foundData = True
                
        return dic if foundData else False


# --- WORKER FUNCTION FOR MULTITHREADING ---
def process_single_course(courseN):
    try:
        course = Course(courseN)
        # Fetch main course page
        overviewResp = respObj("http://kurser.dtu.dk/course/" + courseN + "/info")

        if overviewResp:
            soup = BeautifulSoup(overviewResp, "html.parser")
            links = soup.find_all('a')
            for link in links:
                l = link.get('href')
                if not l: continue
                if "evaluering" in l:
                    course.reviewLinks.append(l)
                elif "karakterer" in l:
                    course.gradeLinks.append(l)

        # Gather data (this makes the sub-requests)
        crawl = course.gather()
        
        if crawl:
            # If we found data, fetch the course name to make it pretty
            soup = BeautifulSoup(respObj("http://kurser.dtu.dk/course/" + courseN), "html.parser")
            h2_tags = soup.find_all('h2')
            if h2_tags:
                try:
                    # Robust name extraction
                    content = h2_tags[0].get_text().strip()
                    parts = content.split(" ", 1)
                    courseName = parts[1] if len(parts) > 1 else content
                    crawl["name"] = courseName
                    return (courseN, crawl)
                except:
                    return (courseN, crawl) # Return data even if name fails
            return (courseN, crawl)
            
    except Exception as e:
        printlog(f"Error processing {courseN}: {str(e)}")
    
    return None

# --- MAIN EXECUTION ---
courseDic = {}
print(f"Starting scraping of {len(courses)} courses using {MAX_WORKERS} threads...")

# ThreadPoolExecutor handles the parallelism
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    # Submit all courses as tasks
    future_to_course = {executor.submit(process_single_course, c): c for c in courses}
    
    # Process as they complete (with progress bar)
    for future in tqdm(concurrent.futures.as_completed(future_to_course), total=len(courses)):
        result = future.result()
        if result:
            c_num, c_data = result
            courseDic[c_num] = c_data

print("Scraping finished. Saving data...")

with open('coursedic.json', 'w') as outfile:
    json.dump(courseDic, outfile)

print(f"Done! Data saved for {len(courseDic)} courses.")
print("--- %s seconds ---" % (time.time() - start_time))