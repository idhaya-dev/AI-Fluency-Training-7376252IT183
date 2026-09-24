COURSE_FEES = {
    "CS101": 30000,
    "AI202": 40000,
    "DS303": 35000
}


def get_course_fee(course_code):
    course_code = course_code.upper()

    if course_code in COURSE_FEES:
        return f"The fee for {course_code} is ₹{COURSE_FEES[course_code]:,}."

    return f"Course {course_code} was not found."