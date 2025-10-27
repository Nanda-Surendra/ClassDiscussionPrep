import pandas as pd
import requests
import streamlit as st
from typing import Dict, List, Any

# --- Configuration ---
FASTAPI_BASE_URL = "http://localhost:8000"

# Functionality configurations
FUNCTIONALITIES = {
    "FindPrerequisites": {
        "endpoint": "find_prerequisites",
        "title": "Course Prerequisites Finder",
        "page_title": "Course Prerequisites",
        "fields": [
            {"name": "subjectCode", "label": "Subject Code"},
            {"name": "courseNumber", "label": "Course Number"}
        ],
        "button_text": "Find Prerequisites",
        "empty_message": "No prerequisites found.",
        "result_type": "dataframe"
    },
    "GetCoursesOffered": {
        "endpoint": "find_current_semester_course_offerings",
        "title": "Course Offerings Finder",
        "page_title": "Course Offered",
        "fields": [
            {"name": "subjectCode", "label": "Subject Code"},
            {"name": "courseNumber", "label": "Course Number"}
        ],
        "button_text": "Get Courses Offered",
        "empty_message": "No courses offered found.",
        "result_type": "dataframe"
    },
    "CheckIfCompletedPrerequisites": {
        "endpoint": "check_if_student_has_taken_all_prerequisites_for_course",
        "title": "Check If Completed Prerequisites",
        "page_title": "Check If Completed Prerequisites",
        "fields": [
            {"name": "studentID", "label": "Student ID"},
            {"name": "subjectCode", "label": "Subject Code"},
            {"name": "courseNumber", "label": "Course Number"}
        ],
        "button_text": "Check If Completed Prerequisites",
        "empty_message": "Student has completed all prerequisites for the course.",
        "result_type": "dataframe"
    },
    "EnrollInCourseOffering": {
        "endpoint": "enroll_student_in_course_offering",
        "title": "Enroll In Course Offering",
        "page_title": "Enroll In Course Offering",
        "fields": [
            {"name": "studentID", "label": "Student ID"},
            {"name": "courseOfferingID", "label": "Course Offering ID"}
        ],
        "button_text": "Enroll In Course Offering",
        "result_type": "enrollment_status",
        "success_condition": {"column": "EnrollmentSucceeded", "value": 1},
        "success_message": "Enrollment successful.",
        "error_message": "Enrollment failed."
    },
    "GetStudentEnrolledCourseOfferings": {
        "endpoint": "get_student_enrolled_course_offerings",
        "title": "Get Student Enrolled Course Offerings",
        "page_title": "Get Student Enrolled Course Offerings",
        "fields": [
            {"name": "studentID", "label": "Student ID"}
        ],
        "button_text": "Get Student Enrolled Course Offerings",
        "empty_message": "No courses enrolled.",
        "result_type": "dataframe"
    },
    "DropFromCourseOffering": {
        "endpoint": "drop_student_from_course_offering",
        "title": "Drop From Course Offering",
        "page_title": "Drop From Course Offering",
        "fields": [
            {"name": "studentID", "label": "Student ID"},
            {"name": "courseOfferingID", "label": "Course Offering ID"}
        ],
        "button_text": "Drop From Course Offering",
        "result_type": "drop_status",
        "success_condition": {"column": "EnrollmentStatus", "value": "Dropped"},
        "success_message": "Drop successful.",
        "error_message": "Drop failed."
    }
}

def fetch_data(service_url: str, params: dict) -> pd.DataFrame:
    """Call FastAPI endpoint and return a DataFrame."""
    response = requests.get(service_url, params=params)
    payload = response.json()
    rows = payload.get("data", [])
    return pd.DataFrame(rows)

def create_form_fields(fields: List[Dict[str, str]]) -> Dict[str, str]:
    """Create form fields dynamically and return the values."""
    field_values = {}
    
    if len(fields) == 1:
        # Single field - no columns needed
        field = fields[0]
        field_values[field["name"]] = st.text_input(
            field["label"], 
            placeholder=field["placeholder"], 
            max_chars=20
        )
    else:
        # Multiple fields - use columns
        cols = st.columns(len(fields))
        for i, field in enumerate(fields):
            with cols[i]:
                field_values[field["name"]] = st.text_input(
                    field["label"], 
                    placeholder=field["placeholder"], 
                    max_chars=20
                )
    
    return field_values

def handle_result(df: pd.DataFrame, config: Dict[str, Any]) -> None:
    """Handle the result based on the configuration."""
    if config["result_type"] == "dataframe":
        st.subheader("Results")
        if df.empty:
            st.info(config["empty_message"])
        else:
            st.dataframe(df, use_container_width=True)
    
    elif config["result_type"] == "enrollment_status":
        if df[config["success_condition"]["column"]].values[0] == config["success_condition"]["value"]:
            st.success(config["success_message"])
        else:
            st.error(config["error_message"])
            st.write(df["EnrollmentResponse"].values[0])
    
    elif config["result_type"] == "drop_status":
        if df[config["success_condition"]["column"]].values[0] == config["success_condition"]["value"]:
            st.success(config["success_message"])
        else:
            st.error(config["error_message"])

def render_functionality_page(functionality: str) -> None:
    """Render the page for a specific functionality."""
    config = FUNCTIONALITIES[functionality]
    
    # Set page config
    st.set_page_config(page_title=config["page_title"], layout="centered")
    st.title(config["title"])
    
    # Create form
    with st.form("search_form", clear_on_submit=False):
        field_values = create_form_fields(config["fields"])
        submitted = st.form_submit_button(config["button_text"])
    
    # Handle form submission
    if submitted:
        service_url = f"{FASTAPI_BASE_URL}/{config['endpoint']}"
        df = fetch_data(service_url, field_values)
        handle_result(df, config)

# --- Sidebar ---
with st.sidebar:
    st.title("Course Recommender Functionalities")
    functionality = st.selectbox("Functionality", list(FUNCTIONALITIES.keys()))
    st.session_state.functionality = functionality


# --- Main Content ---
render_functionality_page(st.session_state.functionality)
