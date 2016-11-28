# DTU Course Analyzer

##Chrome extension
The following is an explanation of how the values was calculated
Markup : * Average grade
         * Percent passed:The ratio of people who **attended** the exam
         * Course rating percentile: Firstly All course are ranked on the question "Samlet set synes jeg, at kurset er godt / Overall I think the course is good" from course reviews. The [lowest scoring course](https://evaluering.dtu.dk/kursus/11343/123826) gets 0% and the [highest scoring course](https://evaluering.dtu.dk/kursus/26122/106759) gets 100%.
          * Bullet list item 2
##Data gathering and analysis
Data was gathered using a Python script that scraped DTU's coursebase and formatted so that the extension can use it.
