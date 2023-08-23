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

## 