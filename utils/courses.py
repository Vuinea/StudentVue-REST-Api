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
        meeting_days = today_course['@MeetingDays']
        room_name = today_course['room_name']
        teacher = today_course['teacher']
        for all_course in all_courses:
            if all_course["@CourseTitle"] in course_name:
                today_course_names[all_course["@CourseTitle"]] = {"start_time": start_time, "end_time": end_time,
                                                                  "meeting_days": meeting_days, "room_name": room_name,
                                                                  "teacher": teacher}
    return today_course_names


def get_courses(user: StudentVue) -> dict:
    courses = get_full_courses(user)
    filtered_courses = []
    for course in courses:
        course = {
            'period': course['@Period'],
            'course_title': course['@CourseTitle'],
            "room_name": course['@RoomName'],
            "teacher": course['@Teacher'],
            "meeting_days": course['@MeetingDays'],
        }
        filtered_courses.append(course)
    return filtered_courses
