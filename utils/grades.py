from studentvue import StudentVue

from utils.courses import get_course_names


def get_grades(user: StudentVue):
    courses = user.get_gradebook()["Gradebook"]["Courses"]["Course"]
    course_grades = []
    for course in courses:

        # getting the correct course name because otherwise it will give the name with a bunch of numbers
        course_name = course["@Title"]
        for name in get_course_names(user):
            if name in course_name:
                course_name = name

        course_teacher = course["@Staff"]

        marks = course["Marks"]
        # checking if there is a grade already in the grade book
        if "Mark" in marks.keys():
            mark = marks["Mark"]
            course_grade = mark['@CalculatedScoreString']
            raw_course_grade = mark["@CalculatedScoreRaw"]
            assignments = mark["Assignments"]
        else:
            course_grade = "N/A"
            raw_course_grade = 0
            assignments = []
        course_grades.append({
            "course_name": course_name,
            "letter_grade": course_grade,
            "number_grade": raw_course_grade,
            "teacher": course_teacher,
            "assignments": assignments
        })
    return course_grades
