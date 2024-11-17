import streamlit as st
import pandas as pd
import datetime

# Streamlit App
st.title("Internship Hours Tracker")

# User Inputs
st.header("Enter Internship Details")
start_date = st.date_input("Start Date", value=datetime.date.today())
weeks_remaining = st.number_input("Number of Weeks Remaining", min_value=1, max_value=52, value=14)
direct_hours_completed = st.number_input("Direct Hours Completed", min_value=0, value=0)
indirect_hours_completed = st.number_input("Indirect Hours Completed", min_value=0, value=0)

total_direct_hours_required = 260
total_indirect_hours_required = 600

# Calculations
remaining_direct_hours = total_direct_hours_required - direct_hours_completed
remaining_indirect_hours = total_indirect_hours_required - indirect_hours_completed
average_direct_per_week = round(remaining_direct_hours / weeks_remaining)
average_indirect_per_week = round(remaining_indirect_hours / weeks_remaining)

# Display Calculations
st.header("Weekly Hours Requirements")
st.write(f"You need to complete an average of {average_direct_per_week} direct hours per week.")
st.write(f"You need to complete an average of {average_indirect_per_week} indirect hours per week.")

# User Input for Tracking Weekly Progress
st.header("Track Weekly Progress")
weekly_direct_hours = []
weekly_indirect_hours = []

for week in range(1, weeks_remaining + 1):
    st.subheader(f"Week {week}")
    direct_hours = st.number_input(f"Direct Hours for Week {week}", min_value=0, value=0, key=f"direct_{week}")
    indirect_hours = st.number_input(f"Indirect Hours for Week {week}", min_value=0, value=0, key=f"indirect_{week}")
    weekly_direct_hours.append(direct_hours)
    weekly_indirect_hours.append(indirect_hours)

# Calculate Total Hours
st.header("Summary")
total_direct_hours = direct_hours_completed + sum(weekly_direct_hours)
total_indirect_hours = indirect_hours_completed + sum(weekly_indirect_hours)

st.write(f"Total Direct Hours Completed: {total_direct_hours} / {total_direct_hours_required}")
st.write(f"Total Indirect Hours Completed: {total_indirect_hours} / {total_indirect_hours_required}")

if total_direct_hours >= total_direct_hours_required and total_indirect_hours >= total_indirect_hours_required:
    st.success("Congratulations! You have completed all required hours.")
elif total_direct_hours >= total_direct_hours_required:
    st.info("You have completed all direct hours but still need to complete indirect hours.")
elif total_indirect_hours >= total_indirect_hours_required:
    st.info("You have completed all indirect hours but still need to complete direct hours.")
else:
    st.warning("You still need to complete both direct and indirect hours.")
