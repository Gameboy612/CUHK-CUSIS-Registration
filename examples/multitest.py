import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from modules.bruteforce import createPDF, printAndOptimizeCourses

createPDF(
    output_file="output/sem2.pdf",
    scheduleRanker=printAndOptimizeCourses(
        courseList = [
                "ENGG2020"
            ],
        year = 2023,
        term = 2,
        maxData = 100,
        showTimetable = False,
        courseListVerbose=False,
        showCoursesVerbose=False,
        saveExcel=False,
        askBeforeSave=False,
        listTimetables=False
    )
)