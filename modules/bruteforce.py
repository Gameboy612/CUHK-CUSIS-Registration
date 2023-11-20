# %%
class EnumTime:
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    L1 = 0
    L2 = 1
    L3 = 2
    L4 = 3
    L5 = 4
    L6 = 5
    L7 = 6
    L8 = 7
    L9 = 8
    L10 = 9

class TimeFrame:
    # t0 and t1 is inclusive
    def __init__(self, t0, t1):
        self.t0 = t0
        self.t1 = t1

    def compare(self, other) -> bool:
        """Compares whether the two TimeFrames are the same.

        Args:
            other (TimeFrame): Comparing TimeFrame

        Returns:
            bool
        """
        return self.t0 == other.t0 and self.t1 == other.t1

class Lesson:
    def __init__(self, name, dayOfWeek, timeFrame, address, type):
        self.Name = name
        self.TimeFrame = timeFrame
        self.DayOfWeek = dayOfWeek
        self.Address = address
        self.type = type

    # isAvailable(Lessons{List}: `The current Timetable`)
    def isAvailable(self, Lessons):
        for i in range(self.TimeFrame.t0, self.TimeFrame.t1 + 1):
            if Lessons[i] != None:
                return False
        return True
    
    # regLesson(fullSchedule{FullSchedule}: `The full schedule`)
    # Overrides the time period to register
    def regLesson(self, fullSchedule):
        daySchedule = fullSchedule.Schedule[self.DayOfWeek]
        for i in range(self.TimeFrame.t0, self.TimeFrame.t1 + 1):
            daySchedule.Lessons[i] = self

    # unregLesson(fullSchedule{FullSchedule}: `The full schedule`)
    # Erases the lesson
    def unregLesson(self, fullSchedule):
        daySchedule = fullSchedule.Schedule[self.DayOfWeek]
        for i in range(self.TimeFrame.t0, self.TimeFrame.t1 + 1):
            if daySchedule.Lessons[i] == self:
                daySchedule.Lessons[i] = None
    
    def compare(self, x):
        return self.TimeFrame.compare(x.TimeFrame)


class DaySchedule:
    Lessons = None
    def __init__(self):
        self.Lessons = [None for i in range(10)]



class FullSchedule:
    Schedule = None
    def __init__(self):
        self.Schedule = [DaySchedule() for i in range(6)]
    
    def getLessonObject(self, weekday, time):
        return self.Schedule[weekday].Lessons[time]
    
    def destructObject(self):
        def getName(y):
            if y != None:
                return y.Name
            return ""
        return [[getName(y) for y in x.Lessons] for x in self.Schedule]

    # This function returns an artificial rating for how good a schedule is.
    def getScheduleRating(self):
        # Free Day Bonus
        def freeDayBonus():
            FREE_DAY_BONUS = 2000
            for d in schedule:
                if all(x is None for x in d):
                    return 0
            return FREE_DAY_BONUS

        # Seperated Lessons and Lesson Counts
        def timeBonus():
            SEPERATION_PENALTY = -50
            LESSON_COUNT_BONUS = 200
            LITTLE_LESSON_PENALTY = -500
            MANY_LESSON_PENALTY = -500
            NO_LUNCH_PENALTY = -30000
            LESSON_PENALTY = -2000

            LESSON_RANGE = (3, 4)

            LUNCH_BREAK = (EnumTime.L4, EnumTime.L7)

            import random
            total = random.randint(0, 1000)
            for d in schedule:
                empty_streak = -1
                lesson_count = 0
                have_lunch = False
                for i in range(len(d)):
                    if d[i] == None and empty_streak != -1:
                        empty_streak += 1
                    if d[i] != None:
                        # empty_streak is squared, to amplify the penalty for separated lessons
                        total += empty_streak * empty_streak * SEPERATION_PENALTY
                        lesson_count += 1
                    if LUNCH_BREAK[0] <= i <= LUNCH_BREAK[1] and d[i] == None:
                        have_lunch = True

                # lesson_count is squared, to amplify the reward for more lessons a day
                if 1 <= lesson_count <= LESSON_RANGE[0]:
                    dl = LESSON_RANGE[0] - lesson_count
                    total += dl * dl * LITTLE_LESSON_PENALTY
                elif lesson_count >= LESSON_RANGE[1]:
                    dl = lesson_count - LESSON_RANGE[1]
                    total += dl * dl * MANY_LESSON_PENALTY
                total += lesson_count * lesson_count * LESSON_COUNT_BONUS
                total += lesson_count * LESSON_PENALTY
                

                # Lunch Penalty
                if not have_lunch:
                    total += NO_LUNCH_PENALTY
            return total
        
        # ...
        schedule = [x.Lessons for x in self.Schedule]
        rating = 100000
        
        rating += freeDayBonus()
        rating += timeBonus()
        
        return rating

class Course:
    AllLessons = None

    # lessons{List[Lesson]}
    def __init__(self, lessons):
        self.AllLessons = lessons
    
    def isAvailable(self, fullSchedule):
        for Lesson in self.AllLessons:
            dayOfWeekSchedule = fullSchedule.Schedule[Lesson.DayOfWeek]
            Lessons = dayOfWeekSchedule.Lessons
            if not Lesson.isAvailable(Lessons):
                return False
        return True
    
    # regCourse(fullSchedule{FullSchedule})
    # return False: Course not available
    # return True: Course successfully applied
    def regCourse(self, fullSchedule):
        if not self.isAvailable(fullSchedule):
            return False
        
        for Lesson in self.AllLessons:
            Lesson.regLesson(fullSchedule)
        return True
    
    # unregCourse(fullSchedule{FullSchedule})
    def unregCourse(self, fullSchedule):
        for Lesson in self.AllLessons:
            Lesson.unregLesson(fullSchedule)


# %% [markdown]
# # Using the Classes

# %% [markdown]
# ## Example of how a course is defined:
# 
# ```
# ENGG1003AA = Course([
#     Lesson("ENGG1003AA - LEC", EnumTime.Monday, TimeFrame(EnumTime.L1, EnumTime.L2), "Lady Shaw Bldg C1"),
#     Lesson("ENGG1003AA - LAB", EnumTime.Monday, TimeFrame(EnumTime.L3, EnumTime.L3), "Lady Shaw Bldg C1")
# ])
# 
# ENGG1003AA.regCourse(fullSchedule)
# ```

# %%
# fullSchedule = FullSchedule()

# ENGG1003AA = Course([
#     Lesson("ENGG1003AA - LEC", EnumTime.Monday, TimeFrame(EnumTime.L1, EnumTime.L2), "Lady Shaw Bldg C1"),
#     Lesson("ENGG1003AA - LAB", EnumTime.Monday, TimeFrame(EnumTime.L3, EnumTime.L3), "Lady Shaw Bldg C1")
# ])

# ENGG1003AA.regCourse(fullSchedule)


# %% [markdown]
# ## Example of how to get a lesson from the schedule:
# 
# ```
# print(fullSchedule.getLessonObject(EnumTime.Monday, EnumTime.L1).Name)
# ```

# %%
# print(fullSchedule.getLessonObject(EnumTime.Monday, EnumTime.L1).Name)

# %% [markdown]
# # Class Wishlist
# In this section, we will be making a class wishlist, where the user can get to choose which classes they want to attend, and which to optimize for.

# %%
class ScheduleRanker:
    def __init__(self, maxData):
        self.MaxData = maxData
        self.Data = list()
        self.RatingData = list()

    def register_data(self, newData):
        rating = newData["rating"]
        if rating not in self.RatingData:
            self.RatingData.append(rating)
            self.RatingData.sort(reverse=True)

            self.Data.append(newData)
            self.Data.sort(key=lambda x: x["rating"], reverse=True)
            if len(self.Data) > self.MaxData:
                self.RatingData = self.RatingData[:self.MaxData]
                self.Data = self.Data[:self.MaxData]
    
    def get_ordered_data(self):
        return self.Data

class CourseChoices:
    def __init__(self, courses):
        self.Courses = courses
    
    def branchCourse(self, fullSchedule, courselist, i, l, scheduleRanker, verbose=True):
        if i == l - 1:
            topscore = {"rating": -1000000, "layout": None}
            for course in self.Courses:
                success = course.regCourse(fullSchedule)
                if not success:
                    continue
                rating = fullSchedule.getScheduleRating()
                layout = fullSchedule.destructObject()
                course.unregCourse(fullSchedule)

                if rating > topscore["rating"]:
                    topscore = {"rating": rating, "layout": layout}

            return topscore
        
        # Branch here:
        topscore = {"rating": -1000000, "layout": None}

        for course in self.Courses:
            # Try to register to course
            success = course.regCourse(fullSchedule)
            if not success:
                continue
            # If course registered, go forward a branch
            output = courselist[i+1].branchCourse(fullSchedule, courselist, i+1, l, scheduleRanker=scheduleRanker, verbose=verbose)

            if output["layout"] != None:
                scheduleRanker.register_data(output)
            # Test if the output is top rating. If yes, then save it.
            if output["rating"] > topscore["rating"]:
                topscore = output
                if verbose:
                    print(topscore)
            course.unregCourse(fullSchedule)
        
        return topscore

# %%
class WishList:
    def __init__(self, default = None):
        if default == None:
            self.AllCourseChoice = list()
        else:
            self.AllCourseChoice = default
    
    def addCourseChoice(self, courseChoice):
        self.AllCourseChoice.append(courseChoice)
    
    def loadCourse(self, fullSchedule, maxData, verbose=True):
        clist = self.AllCourseChoice
        count = len(clist)
        scheduleRanker = ScheduleRanker(maxData)
        return scheduleRanker, clist[0].branchCourse(fullSchedule, clist, 0, count, scheduleRanker=scheduleRanker, verbose=verbose)


# %% [markdown]
# # Testing the program
# Here, we steal CUTS's API to search for our program :D:D:D:D
# 
# 現在，我們要當寄生蟲 :D:D
# 
# https://cuts.hk/ajax_planner2_get_course.php?year=2023&term=1&key=KEYWORDHERE&mode=code

# %%
# CourseList = ["ENGG1110", "AIST1000", "MATH1510", "PHYS1003", "ENGG1003EB", "CHLT1001", "UGFH1000"]

# YEAR = 2023
# TERM = 1

# %%
import requests
from modules.caching import cache
import json

def get_api(courseList, year, term, verbose):
    def api(search_term):
        return f"https://cuts.hk/ajax_planner2_get_course.php?year={year}&term={term}&key={search_term}&mode=code"

    
    @cache
    def fetch_api(website_link):
        return json.dumps(requests.get(website_link).json())
    dayconvert = {
        "M": 0,
        "T": 1,
        "W": 2,
        "H": 3,
        "F": 4,
        "S": 5
    }


    def splitup_tutorials(lessons: list) -> dict:
        """Splits up the given lessons into different tutorial CourseLists.

        Args:
            lessons (list): List of Lessons.

        Returns:
            dict: Example: `{"01": [], "02": []}` 
        """
        def isDuplicateTutorial(lesson: Lesson, tutorial_number: str, other_lessons: dict):
            for x in other_lessons[tutorial_number]:
                if lesson.compare(x) and tutorial_number == x.type.split("/")[2]:
                    return True
            return False

        def isDuplicateLecture(lesson: Lesson, lectures: list):
            for x in lectures:
                if lesson.compare(x):
                    return True
            return False

        lectures = []
        other_lessons = {}
        for lesson in lessons:
            splits = lesson.type.split("/")

            # TUT/MP3/01
            lesson_type = splits[0]
            tutorial_number = splits[2]

            # This checks for whether a non lecture lesson exists in the tutorial no.
            if lesson_type != "LEC":
                # Initialize class
                if not (tutorial_number in other_lessons.keys()):
                    other_lessons[tutorial_number] = []
                if not isDuplicateTutorial(lesson, tutorial_number, other_lessons):
                    other_lessons[tutorial_number].append(lesson)
            else:
                if not isDuplicateLecture(lesson, lectures):
                    lectures.append(lesson)
        
        for lecture in lectures:
            for key in other_lessons.keys():
                other_lessons[key].append(lecture)
        
        return other_lessons

    all_courses = list()
    for course in courseList:
        data = json.loads(fetch_api(api(course)))
        if verbose:
            print(data)
        courses = []
        for coursedata in data["courses"]:
            lessons = []
            timecodes = []
            for perioddata in coursedata["periods"]:
                day = perioddata['day']
                start = perioddata['start'] - 1
                end = perioddata['end'] - 1

                timecode = f"{day}{start}{end}"
                if timecode in timecodes:
                    continue
                if day == "Z":
                    continue
                lessons.append(Lesson(
                    name=f"{coursedata['coursecode']}[{coursedata['unit']}] ({perioddata['type']})",
                    type=perioddata['type'],
                    dayOfWeek=dayconvert[day],
                    timeFrame=TimeFrame(
                        t0=start,
                        t1=end,
                    ),
                    address=perioddata['venue']
                ))
            
            tutorials = splitup_tutorials(lessons)
            
            for tutorial in tutorials.keys():
                courses.append(Course(tutorials[tutorial]))
        all_courses.append(CourseChoices(courses))
    return all_courses

        

# %%
def optimizeCourses(courseList, maxData, year, term, verbose=False):
    wishlist = WishList(get_api(courseList, year, term, verbose=verbose))

    schedule = FullSchedule()
    return wishlist.loadCourse(schedule, maxData=maxData, verbose=verbose)

# %%
def giveCodes(json):
    output = ""
    subjects = []
    if json["layout"] == None:
        return "Not Found Error"
    for x in json["layout"]:
        for y in x:
            if y != "":
                subjects.append(y[0:(y.index(" "))])
    # insert the list to the set
    list_set = set(subjects)

    # convert the set to the list
    unique_list = (list(list_set))

    total_credit = 0
    output += f"Rating: {json['rating']} ({len(unique_list)})\nTotal Lesson Count: {len(subjects)}\n"
    for x in unique_list:
        total_credit += int(x[-2])
        output += "\n" + x

    output += f"\n\nTotal Credit: {total_credit}"

    return output

# %%
import pandas as pd
import numpy as np
import datetime

def showCourseTimetable(scheduleInfo, showCoursesVerbose=False, saveExcel=False, askBeforeSave=True):
    if showCoursesVerbose:
        print(giveCodes(scheduleInfo))
    
    # Define the days of the week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # Define your 2D array
    array_2d = scheduleInfo["layout"]

    # Transpose the array
    transposed_array = np.transpose(array_2d)

    # Create a DataFrame from the transposed array
    df = pd.DataFrame(transposed_array, columns=days_of_week, index=[
        '1 - 08:30',
        '2 - 09:30',
        '3 - 10:30',
        '4 - 11:30',
        '5 - 12:30',
        '6 - 13:30',
        '7 - 14:30',
        '8 - 15:30',
        '9 - 16:30',
        '10 - 17:30'
    ])

    # Create a styler object for the DataFrame
    styler = df.style

    # Define a function to apply color coding
    def color_code(val):
        if val.startswith("CSCI"):
            return "background-color: red"
        if val != "":
            return 'background-color: green'
        else:
            return ''

    # Apply the color coding to the DataFrame styler
    styled_df = styler.applymap(color_code)

    try:
        display(styled_df)
    except:
        print("Unable to display the timetable.")

    ct = datetime.datetime.now()

    # Check if we want to save
    save = saveExcel
    if askBeforeSave:
        isSave = input("Do you want to save this timetable? (y/n)")
        if isSave.lower() == "y":
            save = True
    # Save the table to an Excel file
    if save:
        styled_df.to_excel(f"output/result_{ct.year}-{ct.month}-{ct.day}+{ct.hour}_{ct.minute}_{ct.second}.xlsx", index=False)

# %%
from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode


def getCourseTimetablePDF(pdf, i, m, scheduleInfo, showCoursesVerbose=False, saveExcel=False, askBeforeSave=True):
    codes = giveCodes(scheduleInfo)
    
    pdf.add_page()
    if showCoursesVerbose:
        for i, x in enumerate(codes.split("\n")):
            x = " [".join(x.split("["))
            if "[" in x:
                pdf.set_font('helvetica', '', 10)
                pdf.cell(60, 4, x, new_x="LMARGIN", new_y="NEXT")
            elif x == "":
                pdf.ln(2)
            elif i == 0:
                pdf.set_font('helvetica', 'B', 16)
                pdf.cell(60, 4, x, new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.set_font('helvetica', '', 12)
                pdf.cell(60, 10, x, new_x="LMARGIN", new_y="NEXT")
        
        pdf.ln(2)

    
    # Define the days of the week
    days_of_week = ['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    number_of_lessons = [
        '1\n08:30',
        '2\n09:30',
        '3\n10:30',
        '4\n11:30',
        '5\n12:30',
        '6\n13:30',
        '7\n14:30',
        '8\n15:30',
        '9\n16:30',
        '10\n17:30'
    ]

    # Define your 2D array
    array_2d = scheduleInfo["layout"]
    array_2d.insert(0, number_of_lessons)
    
    transposed_array = list(np.transpose(array_2d))
    transposed_array.insert(0, days_of_week)
    # Transpose the array

    # Get Data
    data = list(transposed_array)

    pdf.set_draw_color(255, 0, 0)
    pdf.set_line_width(0.3)
    pdf.set_font('helvetica', 'U', 10)
    headings_style = FontFace(emphasis="BOLD", color=255, fill_color=(255, 100, 0))
    with pdf.table(
        borders_layout="NO_HORIZONTAL_LINES",
        cell_fill_color=(224, 235, 255),
        cell_fill_mode=TableCellFillMode.ROWS,
        col_widths=(40, 80, 80, 80, 80, 80, 80),
        headings_style=headings_style,
        line_height=6,
        text_align=("CENTER", "CENTER", "CENTER", "CENTER", "CENTER", "CENTER", "CENTER"),
        width=170,
    ) as table:
        for data_row in data:
            row = table.row()
            for datum in data_row:
                row.cell(" [".join(datum.split("[")))
                
    

def createPDF(output_file, scheduleRanker):
    rank = scheduleRanker.get_ordered_data()
    m = len(rank)
    
    # Start a PDF
    pdf = FPDF()
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    pdf.set_top_margin(20)
    pdf.set_auto_page_break(5)

    for i in range(0, m):
        
        getCourseTimetablePDF(pdf, i, m, rank[i], showCoursesVerbose=True, askBeforeSave=False)
        
    pdf.output(output_file)
    

# %%
def printAndOptimizeCourses(courseList, year, term, maxData=100, showTimetable=True, courseListVerbose=False, showCoursesVerbose=False, saveExcel=False, askBeforeSave=False, listTimetables=False):

    scheduleRanker, best = optimizeCourses(
        courseList = courseList,
        year = year,
        term = term,
        maxData = maxData,
        verbose=courseListVerbose
    )
    if showTimetable:
        showCourseTimetable(best, showCoursesVerbose=courseListVerbose, saveExcel=saveExcel, askBeforeSave=askBeforeSave)

    if listTimetables:
        rank = scheduleRanker.get_ordered_data()
        m = len(rank)
        for i in range(0, m):
            print(f"{i + 1}/{m}")
            showCourseTimetable(rank[i], showCoursesVerbose=True, askBeforeSave=False)

    return scheduleRanker

# %% [markdown]
# # Optimizing our courses!!!
# 
# Here, enter your courseList, year, and term, to start finding your most optimal class schedules.

# %%
# createPDF(
#     output_file="output/sem1.pdf",
#     scheduleRanker=printAndOptimizeCourses(
#         courseList = [
#                 "ENGG1110",
#                 "AIST1000",
#                 "MATH1510",
#                 "PHYS1003",
#                 "ENGG1003EB",
#                 "CHLT1001",
#                 "PHED1017"
#             ],
#         year = 2023,
#         term = 1,
#         maxData = 100,
#         showTimetable = False,
#         courseListVerbose=False,
#         showCoursesVerbose=False,
#         saveExcel=False,
#         askBeforeSave=False,
#         listTimetables=False
#     )
# )

# %%
createPDF(
    output_file="output/sem1.pdf",
    scheduleRanker=printAndOptimizeCourses(
        courseList = [
                "ENGG1110",
                "AIST1000"
            ],
        year = 2023,
        term = 1,
        maxData = 100,
        showTimetable = True,
        courseListVerbose=False,
        showCoursesVerbose=False,
        saveExcel=False,
        askBeforeSave=False,
        listTimetables=False
    )
)



