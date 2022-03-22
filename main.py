from fastapi import FastAPI
from studentvue import StudentVue

from utils.courses import get_today_courses, get_courses
from utils.grades import get_grades
from utils.assignments import get_assignments, get_weighted_assignments
from utils.events import get_events, get_all_events, get_today_events


from local_settings import USERNAME, PASSWORD

app = FastAPI()

user = StudentVue(USERNAME, PASSWORD, "portal.lcps.org")



@app.get("/courses")
async def courses(today: bool = True):
    if today:
        # if there is no school that day then a key error will pop up, so I am checking weather it is a holiday
        try:
            return get_today_courses(user)
        except KeyError:
            pass
    return get_courses(user)


@app.get("/courses/{course_id}")
async def course(course_id: int):
    return get_courses(user)[course_id]


@app.get("/grades")
async def grades():
    return get_grades(user)


@app.get("/grades/{course_id}")
async def course_grades(course_id: int):
    return get_grades(user)[course_id]


@app.get("/assignments")
async def assignments(weighted: bool = False):
    a_list = get_assignments(user) if not weighted else get_weighted_assignments(user)
    return a_list


@app.get("/assignments/{course_id}")
async def course_assignments(course_id: int, weighted: bool = False):
    a_list = get_assignments(user) if not weighted else get_weighted_assignments(user)
    return a_list[course_id]


@app.get("/events")
async def events():
    return get_events(user)


@app.get("/events/{filter}")
async def filtered_events(filter: str):
    if filter == "all":
        return get_all_events(user)
    elif filter == "today":
        return get_today_events(user)
