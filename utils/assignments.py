from studentvue import StudentVue


def format_assignment_name(assignment_name: str):
    assignment_name = assignment_name.strip()
    number_start = assignment_name.find("(")

    return assignment_name[0:number_start]


def get_assignments(user: StudentVue) -> list:
    courses = user.get_gradebook()["Gradebook"]["Courses"]["Course"]
    courses_with_assignments = []
    for course in courses:
        assignments = []

        title = format_assignment_name(course['@Title']).strip()
        raw_assignments = course["Marks"]['Mark']['Assignments']["Assignment"]
        if not isinstance(raw_assignments, list):
            raw_assignments = [raw_assignments]
        for assignment in raw_assignments:
            # filtering out just the fields I need
            assignment = {
                "measure": assignment["@Measure"],
                "measure_description": assignment["@MeasureDescription"],
                "score": assignment['@Score'],
                "points": assignment["@Points"],
                "type": assignment["@Type"],
                "due_date": assignment["@DueDate"],
                "notes": assignment['@Notes']
            }
            assignments.append(assignment)
        title_and_assignments = [title, assignments]

        courses_with_assignments.append(title_and_assignments)

    return courses_with_assignments


def get_weighted_assignments(user: StudentVue):
    courses = get_assignments(user)
    weighted_assignments = []

    for course in courses:
        # grabbing 1st element because the 0th element is the course name and the second element is the assignments
        course = course[1]
        course_assignments = []
        for a in course:
            if "formative" not in a["type"].lower() and 'not for grading' not in a['type'].lower():
                course_assignments.append(a)

        weighted_assignments.append(course_assignments)

    return weighted_assignments

