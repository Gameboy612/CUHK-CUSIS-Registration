

from modules.bruteforce import createPDF, printAndOptimizeCourses

createPDF(
    output_file="output/sem2.pdf",
    scheduleRanker=printAndOptimizeCourses(
        courseList = [
                "PHED1028A",
                "ENGG2020",
                "ELTU1001CO",
                "ENGG1120E",
                "ENGG1130C",
                "UGFN1000W",
                "UGCP1001",
                "GEUC1000",
                "UGEA1881",
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