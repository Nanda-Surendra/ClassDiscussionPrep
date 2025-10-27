from get_db_connection import get_db_connection

def enroll_student_in_course_offering_alternate(
    studentID: int, 
    courseOfferingID: int
):
    
    conn = get_db_connection()    
    cursor = conn.cursor()
    
    #    enrollmentResponse = cursor.execute("{call procEnrollStudentInCourseOffering(?, ?, ?)}", (studentID, courseOfferingID, cursor.var(pyodbc.SQL_VARCHAR)))
    # Call the stored procedure with output parameters
    sql = """
    DECLARE @enrollmentResponse nvarchar(100);
    DECLARE @enrollmentSucceeded bit;

    EXECUTE @enrollmentSucceeded = procEnrollStudentInCourseOffering
        @studentID = ?,
        @courseOfferingID = ?,
        @enrollmentResponse = @enrollmentResponse OUTPUT;

    SELECT @enrollmentSucceeded AS enrollmentSucceeded, 
        @enrollmentResponse AS enrollmentResponse;
    """
    cursor.execute(sql, (studentID, courseOfferingID))
    row = cursor.fetchone()
    enrollmentResponse = row.enrollmentResponse
    enrollmentSucceeded = row.enrollmentSucceeded

    cursor.close()
    conn.commit()
    conn.close()    

    results = [
        {"EnrollmentResponse": enrollmentResponse, "EnrollmentSucceeded": enrollmentSucceeded}
    ]

    return {
        "data": results
    }
