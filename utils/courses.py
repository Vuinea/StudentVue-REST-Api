from studentvue import StudentVue


# this function will just return the ordered dict
def get_full_courses(user: StudentVue) -> list:
    return user.get_schedule()["StudentClassSchedule"]["ClassLists"]["ClassListing"]


# this function will just return the course names
def get_course_names(user: StudentVue) -> list:
    courses = get_full_courses(user)

    return [course["@CourseTitle"] for course in courses]


def get_raw_today_courses(user: StudentVue) -> list:
    today_courses = \
        user.get_schedule()["StudentClassSchedule"]["TodayScheduleInfoData"]["SchoolInfos"]["SchoolInfo"]["Classes"][
            "ClassInfo"]
    return today_courses


# I have to write this function because when you get the @ClassName it gives some weird numbers at the end
def get_today_courses(user: StudentVue) -> dict:
    all_courses = get_full_courses(user)
    today_courses = get_raw_today_courses(user)

    today_course_names = {}

    for today_course in today_courses:
        course_name = today_course["@ClassName"]
        start_time = today_course["@StartTime"]
        end_time = today_course["@EndTime"]
        for all_course in all_courses:
            if all_course["@CourseTitle"] in course_name:
                today_course_names[all_course["@CourseTitle"]] = {"start_time": start_time, "end_time": end_time}
    return today_course_names

