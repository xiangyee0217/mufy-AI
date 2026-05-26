# ==========================================
# MY FIRST STREAMLT
# ==========================================

import streamlit as st
import csv
import os
from datetime import date, time

# Set page title
st.title("My First Streamlit App")

# Add header
st.header("welcome to the dashboard")
# ==========================================
# FILE SETUP
# ==========================================

FILE_NAME = "tasks.csv"

HEADERS = [
    "Task",
    "Date",
    "Time",
    "Category",
    "Colour",
    "Notes",
    "Completed"
]

# Create file if it doesn't exist
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)

# ==========================================
# FUNCTIONS
# ==========================================

def load_tasks():
    """
    Read all tasks from CSV and return list of dictionaries
    """
    tasks = []

    with open(FILE_NAME, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            tasks.append(row)

    return tasks


def save_task(task_data):
    """
    Append one task to CSV file
    """
    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(task_data)


def mark_complete(task_name):
    """
    Mark a task as completed
    """
    tasks = load_tasks()

    updated_tasks = []

    for task in tasks:
        if task["Task"] == task_name:
            task["Completed"] = "True"

        updated_tasks.append(task)

    # Rewrite file
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(updated_tasks)


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(page_title="Student Planner", layout="wide")

st.title("📚 Student Planner (No Pandas Version)")
st.write("Organise your study life easily")

# ==========================================
# SIDEBAR - ADD TASK
# ==========================================

st.sidebar.header("➕ Add Task")

task = st.sidebar.text_input("Task Name")

task_date = st.sidebar.date_input("Date", value=date.today())

task_time = st.sidebar.time_input("Time", value=time(12, 0))

category = st.sidebar.selectbox(
    "Category",
    ["Study", "Assignment", "Exam", "Personal", "Workout"]
)

colour = st.sidebar.color_picker("Choose Colour", "#00AEEF")

notes = st.sidebar.text_area("Notes")

if st.sidebar.button("Add Task"):

    if task.strip() == "":
        st.sidebar.error("Task name cannot be empty")

    else:
        save_task([
            task,
            str(task_date),
            str(task_time),
            category,
            colour,
            notes,
            "False"
        ])

        st.sidebar.success("Task added!")

# ==========================================
# LOAD TASKS
# ==========================================

tasks = load_tasks()

# ==========================================
# DATE FILTER (CALENDAR FEEL)
# ==========================================

st.header("📅 View Tasks by Date")

selected_date = st.date_input("Select Date", value=date.today())

# filter tasks manually
filtered_tasks = [
    t for t in tasks if t["Date"] == str(selected_date)
]

# ==========================================
# DISPLAY TASKS
# ==========================================

st.header("✅ Tasks for Selected Date")

if not filtered_tasks:
    st.info("No tasks for this date")

else:
    for task in filtered_tasks:

        st.markdown(
            f"""
            <div style="
                background-color:{task['Colour']};
                padding:12px;
                border-radius:10px;
                margin-bottom:10px;
                color:white;
            ">
                <h4>{task['Task']}</h4>
                <p>
                ⏰ {task['Time']} <br>
                📂 {task['Category']} <br>
                📝 {task['Notes']} <br>
                ✔ Completed: {task['Completed']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================
# ALL TASKS
# ==========================================

st.header("📋 All Tasks")

if not tasks:
    st.warning("No tasks yet")

else:
    for t in tasks:
        st.write(
            f"**{t['Task']}** | {t['Date']} | {t['Time']} | "
            f"{t['Category']} | Completed: {t['Completed']}"
        )

# ==========================================
# MARK TASK COMPLETE
# ==========================================

st.header("✔ Mark Task Complete")

task_names = [t["Task"] for t in tasks]

if task_names:

    selected_task = st.selectbox("Choose task", task_names)

    if st.button("Mark as Completed"):
        mark_complete(selected_task)
        st.success("Task updated!")
else:
    st.info("No tasks available")

# ==========================================
# COMPLETED TASKS
# ==========================================

st.header("🎉 Completed Tasks")

completed = [t for t in tasks if t["Completed"] == "True"]

if not completed:
    st.info("No completed tasks yet")

else:
    for t in completed:
        st.write(f"✔ {t['Task']} ({t['Date']})")