# DTU Course Analyzer
The data is provided as is, with no guarentee and responsibility for its correctness.


## Installation
https://chrome.google.com/webstore/detail/dtu-course-analyzer/bimhgdngikcnelkhjindmdghndfmdcde
https://addons.mozilla.org/en-US/firefox/addon/dtu-course-analyzer/

## Chrome extension
The following is an explanation of how the values were calculated (higher is better)
  * Average grade
  * Average grade percentile: All courses are ranked against eachother based on average grade. 
  * Percent passed: The ratio of people who **attended** the exam that passed.
  * Course rating percentile: All course are ranked based on the question "Overall I think the course is good" from course reviews. 
  * Workscore percentile: Ranked based on the question "5 points are allocated to 9h./week (45 h./week in the 3-week period). I think my workload in the course is [Much less..Much more]"
  * Lazyscore: The average percentile between percent passed and workload. This is a metric for how much beer one can drink during a semester and still get decent grades. 🍺🍺🍺

## Data gathering and analysis
Data was gathered using a Python script that scraped DTU's coursebase and formatted it so that the extension can use it.

# Development
## Setup
 1. Install python dependencies `pip3 install -r requirements.txt`

## Gather data
 1. Update the list of courses using getCourseNumbers.js
 2. Create a file called `secret.txt` containing the `ASP.NET_SessionId` cookie set when entering https://kurser.dtu.dk. Make sure there is no leading or trailing whitespace and newlines
 3. Run the scraper `python3 scraper.py`
 4. Analyze the data using `python3 analyzer.py extension`
 
## Debugging
### Chrome
 1. Open the extensions page
 2. Enable developer mode (Upper right corner)
 3. Click on "Load unpacked"
 4. Select the `extension` directory  within the project
### Firefox
 0. Install `web-ext`
     - Run `npm install --global web-ext`
 1. In a terminal window, `cd` into the `extension` directory within the project
 2. Run the extension using `web-ext run`

