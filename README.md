# DTU Course Analyzer
So here it is, the brand new version of DTU Course Analyzer with data from the fall courses of 2024.
The extension is provided as is, with no guarentee nor responsibility for its stability and correctness. For more info, see the license.


## Installation

Installation in Chrome:
1. In Chrome, go to https://chromewebstore.google.com/detail/dtu-course-analyzer/bimhgdngikcnelkhjindmdghndfmdcde and install the extension

Installation in Chrome from GitHub
1. Download: https://github.com/SMKIDRaadet/dtu-course-analyzer/archive/refs/tags/v1.3.7.zip
2. In Chrome, go to the page: chrome://extensions/
3. Enable developer mode
4. Click on "Load unpacked" and select the "extension" folder in what you downloaded in step 1

Installation in Safari (iPhone and iPad):
1. Compile the Safari extension located at https://github.com/SMKIDRaadet/dtu-course-analyzer/tree/master/Safari%20extension in Xcode
2. Open the app
3. In Safari, press the "Aa" button in the address bar
4. Tap "Manage Extensions" and enable the extension
5. Go to a course on kurser.dtu.dk
6. Tap the "Aa" button in the address bar
7. Tap DTU Course Analyzer and give it permission to modify kurser.dtu.dk

Installation in Safari (Mac):
1. Compile the Safari extension located at https://github.com/SMKIDRaadet/dtu-course-analyzer/tree/master/Safari%20extension in Xcode
2. Open the app
3. In Safari, open settings
4. Go to the "Extensions" tab and enable the extension
5. Click on "Manage Extensions" and enable the extension
6. Go to a course on kurser.dtu.dk
7. Click on DTU Course Analyzer in the address bar and give it permission to modify kurser.dtu.dk"

### Google Chrome (old version)
https://chrome.google.com/webstore/detail/dtu-course-analyzer/bimhgdngikcnelkhjindmdghndfmdcde
### Firefox
https://addons.mozilla.org/en-US/firefox/addon/dtu-course-analyzer/, an alternative version managed by [Mathias Herløv Lund](https://github.com/SalisMaxima) is available [here](https://addons.mozilla.org/en-US/firefox/addon/dtu-course-analyzer-2023).

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
 1. Create a file called `secret.txt` containing the `ASP.NET_SessionId` cookie set when you are logged into https://kurser.dtu.dk with a DTU account. Make sure there is no leading or trailing whitespace and newlines.
If you are using Firefox, you can get the cookie by pressing F12, going to the storage tab, and copying the value of the `ASP.NET_SessionId` cookie.
 2. Update the list of courses using `python3 getCourseNumbers.py`
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

