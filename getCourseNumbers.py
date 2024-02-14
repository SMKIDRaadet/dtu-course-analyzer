"""
This file is used to create coursenumbers.txt, which is used in scraper.py.
It connects to kurser.dtu.dk/search using the key from the env var SESSION_ID.
"""
import requests
from bs4 import BeautifulSoup
import os


def key_error(exists=False):
    BOLD = '\033[1m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

    if not exists:
        print(BOLD, WARNING, "No SESSION_ID found in environment variables.", ENDC)
    else:
        print(BOLD, WARNING, "The provided SESSION_ID seems incorrect.", ENDC)

    print(BOLD, WARNING,
          "Add a Github Secrets (see https://docs.github.com/en/actions/security-guides/using-secrets-in-github"
          "-actions#creating-secrets-for-a-repository) named SESSION_ID containing the value of the ASP.NET_SessionId"
          " cookie from kurser.dtu.dk", ENDC)
    exit(-1)


# this url is the url of the search page with all the filters applied
url = "https://kurser.dtu.dk/search?CourseCode=&SearchKeyword=&SchedulePlacement=E1%3BE2%3BE3%3BE4%3BE5%3BE1A%3BE2A%3BE3A%3BE4A%3BE5A%3BE1B%3BE2B%3BE3B%3BE4B%3BE5B%3BE7%3BE&SchedulePlacement=E1%3BE1A%3BE1B&SchedulePlacement=E1A&SchedulePlacement=E1B&SchedulePlacement=E2%3BE2A%3BE2B&SchedulePlacement=E2A&SchedulePlacement=E2B&SchedulePlacement=E3%3BE3A%3BE3B&SchedulePlacement=E3A&SchedulePlacement=E3B&SchedulePlacement=E4%3BE4A%3BE4B&SchedulePlacement=E4A&SchedulePlacement=E4B&SchedulePlacement=E5%3BE5A%3BE5B&SchedulePlacement=E5A&SchedulePlacement=E5B&SchedulePlacement=E7&SchedulePlacement=F1%3BF2%3BF3%3BF4%3BF5%3BF1A%3BF2A%3BF3A%3BF4A%3BF5A%3BF1B%3BF2B%3BF3B%3BF4B%3BF5B%3BF7%3BF&SchedulePlacement=F1%3BF1A%3BF1B&SchedulePlacement=F1A&SchedulePlacement=F1B&SchedulePlacement=F2%3BF2A%3BF2B&SchedulePlacement=F2A&SchedulePlacement=F2B&SchedulePlacement=F3%3BF3A%3BF3B&SchedulePlacement=F3A&SchedulePlacement=F3B&SchedulePlacement=F4%3BF4A%3BF4B&SchedulePlacement=F4A&SchedulePlacement=F4B&SchedulePlacement=F5%3BF5A%3BF5B&SchedulePlacement=F5A&SchedulePlacement=F5B&SchedulePlacement=F7&SchedulePlacement=January&SchedulePlacement=August%3BJuly%3BJune&SchedulePlacement=August&SchedulePlacement=July&SchedulePlacement=June&CourseType=&TeachingLanguage="

key = os.environ.get('SESSION_ID', False)
if not key:
    key_error()

# send a request to the url with the key
r = requests.get(url, cookies={'ASP.NET_SessionId' : key})
soup = BeautifulSoup(r.content, "html.parser")
data = soup.find_all("img" , {"class" : "basketIcon clickable"})

# get the course numbers from the HTML data
courseNumbers = [i['data-coursecode'] for i in data]

if len(courseNumbers) == 0:
    key_error(True)

# Write to file
open('coursenumbers.txt', 'w').write(','.join(courseNumbers))
