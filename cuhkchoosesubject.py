import random

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

class Lesson:
    def __init__(self, name, dayOfWeek, timeFrame, address):
        self.Name = name
        self.TimeFrame = timeFrame
        self.DayOfWeek = dayOfWeek
        self.Address = address

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


class DaySchedule:
    Lessons = None
    def __init__(self):
        self.Lessons = [None for i in range(11)]



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
            NO_LUNCH_PENALTY = -15000
            LESSON_BONUS = 10000

            LESSON_RANGE = [3, 4]

            LUNCH_START = EnumTime.L5
            LUNCH_END = EnumTime.L7

            total = 0
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
                    if LUNCH_START <= i <= LUNCH_END and d[i] == None:
                        have_lunch = True

                # lesson_count is squared, to amplify the reward for more lessons a day
                if 1 <= lesson_count <= LESSON_RANGE[0]:
                    dl = LESSON_RANGE[0] - lesson_count
                    total += dl * dl * LITTLE_LESSON_PENALTY
                elif lesson_count >= LESSON_RANGE[1]:
                    dl = lesson_count - LESSON_RANGE[1]
                    total += dl * dl * MANY_LESSON_PENALTY
                total += lesson_count * lesson_count * LESSON_COUNT_BONUS
                total += lesson_count * LESSON_BONUS
                
                

                # Lunch Penalty
                if not have_lunch:
                    total += NO_LUNCH_PENALTY
            return total
        
        # ...
        schedule = [x.Lessons for x in self.Schedule]
        rating = 10000
        
        rating += freeDayBonus()
        rating += timeBonus()
        rating += random.randint(-100,100)
        
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


fullSchedule = FullSchedule()

class CourseChoices:
    def __init__(self, courses):
        self.Courses = courses
    
    def branchCourse(self, fullSchedule, courselist, i, l):
        if i == l - 1:
            topscore = {"rating": 0, "layout": None}
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
                pass
            # If course registered, go forward a branch
            output = courselist[i+1].branchCourse(fullSchedule, courselist, i+1, l)

            # Test if the output is top rating. If yes, then save it.
            if output["rating"] > topscore["rating"]:
                topscore = output
                print(topscore)
            course.unregCourse(fullSchedule)
        
        return topscore
    
class WishList:
    AllCourseChoice = list()
    def __init__(self, default = list()):
        self.AllCourseChoice = default
    
    def addCourseChoice(self, courseChoice):
        self.AllCourseChoice.append(courseChoice)
    
    def loadCourse(self, fullSchedule):
        clist = self.AllCourseChoice
        count = len(clist)

        return clist[0].branchCourse(fullSchedule, clist, 0, count)
