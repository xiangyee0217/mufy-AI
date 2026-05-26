# ==========================================
# STUDENT PLANNER WEB APP
# ==========================================
# Import librariea
import streamlit as st
import pandas as pd
from datetime import date, time 
import os

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Student Planner",
    page_icon="📚",
    layout="wide"
)

# ==========================================
# FILE SETUP
# ==========================================

TASKS_FILE = "tasks.csv"

# If tasks.csv doesn't exist,
# create an empty dataframe
if not os.path.exists(TASKS_FILE):
    empty_df = pd.DataFrame(columns=[
        "Task",
        "Date",
        "Time",
        "Category",
        "Colour",
        "Notes",
        "Completed"
    ])
    empty_df.to_csv(TASKS_FILE, index=False)

# ==========================================
# FUNCTIONS
# ==========================================

def load_tasks():
    """
    Load tasks from CSV file
    """
    return pd.read_csv(TASKS_FILE)


def save_tasks(df):
    """
    Save tasks into CSV file
    """
    df.to_csv(TASKS_FILE, index=False)


def add_task(task, task_date, task_time,
             category, colour, notes):
    """
    Add a new task into dataframe
    """

    df = load_tasks()

    new_task = {
        "Task": task,
        "Date": task_date,
        "Time": task_time,
        "Category": category,
        "Colour": colour,
        "Notes": notes,
        "Completed": False
    }

    df = pd.concat(
        [df, pd.DataFrame([new_task])],
        ignore_index=True
    )

    save_tasks(df)


# ==========================================
# APP TITLE
# ==========================================

st.title("📚 Student Planner App")
st.write("Organise your studies and daily tasks!")

# ==========================================
# SIDEBAR - ADD TASK
# ==========================================

st.sidebar.header("➕ Add New Task")

task_name = st.sidebar.text_input("Task Name")

task_date = st.sidebar.date_input(
    "Choose Date",
    value=date.today()
)

task_time = st.sidebar.time_input(
    "Choose Time",
    value=time(12, 0)
)

category = st.sidebar.selectbox(
    "Category",
    [
        "Study",
        "Assignment",
        "Exam",
        "Personal",
        "Workout"
    ]
)

colour = st.sidebar.color_picker(
    "Choose Event Colour",
    "#00AEEF"
)

notes = st.sidebar.text_area(
    "Notes"
)

# Add task button
if st.sidebar.button("Add Task"):

    if task_name.strip() == "":
        st.sidebar.error("Task name cannot be empty!")

    else:
        add_task(
            task_name,
            task_date,
            task_time,
            category,
            colour,
            notes
        )

        st.sidebar.success("Task added successfully!")

# ==========================================
# LOAD TASKS
# ==========================================

tasks_df = load_tasks()

# ==========================================
# MAIN PAGE - CALENDAR VIEW
# ==========================================

st.header("📅 Task Calendar")

selected_date = st.date_input(
    "Select a date to view tasks",
    value=date.today()
)

# Filter tasks for selected date
filtered_tasks = tasks_df[
    tasks_df["Date"] == str(selected_date)
]

# ==========================================
# DISPLAY TASKS
# ==========================================

st.header("✅ Tasks For Selected Date")

if filtered_tasks.empty:
    st.info("No tasks for this date.")

else:

    for index, row in filtered_tasks.iterrows():

        # Create coloured task container
        st.markdown(
            f"""
            <div style="
                padding:15px;
                border-radius:10px;
                background-color:{row['Colour']};
                margin-bottom:10px;
                color:white;
            ">
                <h4>{row['Task']}</h4>
                <p>
                ⏰ {row['Time']} <br>
                📂 {row['Category']} <br>
                📝 {row['Notes']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================
# ALL TASKS SECTION
# ==========================================

st.header("📋 All Tasks")

if tasks_df.empty:
    st.warning("No tasks added yet.")

else:

    # Display dataframe
    st.dataframe(tasks_df)

# ==========================================
# MARK TASK COMPLETE
# ==========================================

st.header("✔ Mark Task As Completed")

if not tasks_df.empty:

    task_options = tasks_df["Task"].tolist()

    selected_task = st.selectbox(
        "Choose task",
        task_options
    )

    if st.button("Complete Task"):

        tasks_df.loc[
            tasks_df["Task"] == selected_task,
            "Completed"
        ] = True

        save_tasks(tasks_df)

        st.success("Task marked as completed!")

# ==========================================
# COMPLETED TASKS
# ==========================================

st.header("🎉 Completed Tasks")

completed_tasks = tasks_df[
    tasks_df["Completed"] == True
]

if completed_tasks.empty:
    st.info("No completed tasks yet.")

else:
    st.dataframe(completed_tasks)