#from fastapi import FastAPI                  
#import pyodbc
from get_db_connection import get_db_connection

# app = FastAPI()

# @app.get("/find_current_semester_course_offerings/")
def find_current_semester_course_offerings(
    subjectCode: str,
    courseNumber: str
):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute the stored procedure
    cursor.execute("{call procFindCurrentSemesterCourseOfferingsForSpecifiedCourse(?, ?)}", (subjectCode, courseNumber))

    # Fetch results
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert to list of dicts
    results = [
        {"SubjectCode": row.SubjectCode, "CourseNumber": row.CourseNumber, 
        "CRN": row.CRN, "Semester": row.CourseOfferingSemester, "Year": row.CourseOfferingYear, "CourseOfferingID": row.CourseOfferingID,
        "NumberSeatsRemaining": row.NumberSeatsRemaining}
        for row in rows
    ]
    return {"data": results}