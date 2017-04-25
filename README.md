# DTU Course Analyzer
dtu.course.analyzer@gmail.com

## Chrome extension
The following is an explanation of how the values were calculated
  * Average grade
  * Average grade percentile: All courses are ranked based on average grade. The [course with the lowest average](http://karakterer.dtu.dk/Histogram/1/11343/Summer-2016) gets 0% and [the course with the highest average](http://karakterer.dtu.dk/Histogram/1/11463/Winter-2015) gets 100%.
  * Percent passed: The ratio of people who **attended** the exam that passed.
  * Course rating percentile: All course are ranked based on the question "Samlet set synes jeg, at kurset er godt / Overall I think the course is good" from course reviews. The [lowest scoring course](https://evaluering.dtu.dk/kursus/11343/123826) gets 0% and the [highest scoring course](https://evaluering.dtu.dk/kursus/26122/106759) gets 100%.
  * Workload percentile: Ranked the same way as "Course rating percentile" based on the question "5 point er normeret til 9t./uge (45 t./uge i treugers-perioden). Jeg mener, at min arbejdsindsats i kurset er [Meget mindre..Meget større] / 5 points are allocated to 9h./week (45 h./week in the 3-week period). I think my workload in the course is [Much less..Much bigger"
  * Lazyscore: The average percentile between percent passed and workload. This is a metric for how much beer one can drink during a semester and still get decent grades.
  
## Data gathering and analysis
Data was gathered using a Python script that scraped DTU's coursebase and formatted it so that the extension can use it.
