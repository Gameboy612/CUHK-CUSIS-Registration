# CUHK CUSIS Registration
## This project consists of tools to help assist CUSIS subject selection.

<br><br><br>

# `bruteforce.ipynb`
## Summary:
This notebook allows the users to generate their most optimal course timetable.
## Technical:
There are some factors affecting whether a timetable is optimal:

Bonuses:
1. Free Day Bonus
2. Lesson Count per day Bonus

Penalties:
1. Separation Penalty
2. Too little lesson penalty [1 <= x <= 3] (except free day)
3. Too many lessons penalty [x >= 4]
4. No lunch penalty [Lunch break at L5 to L7, this is configurable]

Randomization:
1. A rating of -5000 to 5000 will be assigned to each timetable, to add randomization to the output, giving a variety of outcomes.

## How to use:
At `Testing the Program`, there is this line of code underneath:
```
CourseList = ["ENGG1110", "AIST1000", "MATH1510", "PHYS1003", "ENGG1003", "CHLT1001"]
```

To select your courses, enter the course name inside this list. An example is already shown above.

After that, click "Run All". In the end of the ipynb, there will be a schedule showing you the most optimal setup. A question box appears to ask whether you want to save this as an excel file.

Type "y" to save the schedule, and type anything else to decline.


## Data Source:
The data source is extracted from [CUTS](https://cuts.hk/ajax_planner2_get_course.php?year=2023&term=1&key=KEYWORDHERE&mode=code).

```
https://cuts.hk/ajax_planner2_get_course.php?year=2023&term=1&key=KEYWORDHERE&mode=code
```

As it is not from official sources, please double confirm the output before assigning the courses.
