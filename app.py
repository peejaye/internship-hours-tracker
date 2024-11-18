import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pydub import AudioSegment
from pydub.playback import play
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

# Streamlit App - Modern Style Enhancements
st.set_page_config(page_title="Internship Hours Tracker", page_icon="📊", layout="wide")

# Custom CSS for Apple-Like Design
st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
            font-family: 'Helvetica Neue', sans-serif;
        }
        h1, h2, h3, h4 {
            font-weight: bold;
            color: #333;
        }
        .stButton>button {
            background-color: #007AFF;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #005BB5;
        }
        .stNumberInput>div>input {
            border-radius: 5px;
            border: 2px solid #007AFF;
        }
    </style>
    """, unsafe_allow_html=True)

# Function to play motivational audio
@st.cache_resource
def play_audio(audio_file):
    sound = AudioSegment.from_file(io.BytesIO(audio_file), format="mp3")
    play(sound)

# User Inputs
st.title("Internship Hours Tracker")
weeks_remaining = st.number_input("Number of Weeks Remaining", min_value=1, max_value=52, value=14, key='weeks_remaining_input')
start_date = st.date_input("Start Date", value=datetime.date.today())
end_date = start_date + datetime.timedelta(weeks=weeks_remaining)
end_date = start_date + datetime.timedelta(weeks=weeks_remaining)
# Removed duplicate weeks_remaining input
# Direct Hours Completed (calculated from weekly inputs)
# Initialize session state to keep track of weekly hours if not already initialized or update if weeks_remaining changes
if "weekly_direct_hours" not in st.session_state or len(st.session_state.weekly_direct_hours) != weeks_remaining:
    st.session_state.weekly_direct_hours = [0] * weeks_remaining
if "weekly_indirect_hours" not in st.session_state or len(st.session_state.weekly_indirect_hours) != weeks_remaining:
    st.session_state.weekly_indirect_hours = [0] * weeks_remaining

# Direct Hours Completed (calculated from weekly inputs)
direct_hours_completed = sum(st.session_state.weekly_direct_hours)
# Indirect Hours Completed (calculated from weekly inputs)
# Indirect Hours Completed (calculated from weekly inputs)
indirect_hours_completed = sum(st.session_state.weekly_indirect_hours)

# Initialize session state to keep track of weekly hours if not already initialized
if "weekly_direct_hours" not in st.session_state:
    st.session_state.weekly_direct_hours = [0] * weeks_remaining
if "weekly_indirect_hours" not in st.session_state:
    st.session_state.weekly_indirect_hours = [0] * weeks_remaining

# Total required hours
total_direct_hours_required = 260
total_indirect_hours_required = 600

# Calculations
remaining_direct_hours = total_direct_hours_required - direct_hours_completed
remaining_indirect_hours = total_indirect_hours_required - indirect_hours_completed
average_direct_per_week = round(remaining_direct_hours / weeks_remaining)
average_indirect_per_week = round(remaining_indirect_hours / weeks_remaining)

# Display Remaining Hours in Red
st.markdown(f"<p style='color:red; font-weight: bold;'>Remaining Direct Hours Needed: {remaining_direct_hours}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='color:red; font-weight: bold;'>Remaining Indirect Hours Needed: {remaining_indirect_hours}</p>", unsafe_allow_html=True)

# Display Calculations
st.header("Weekly Hours Requirements")
st.write(f"You need to complete an average of {average_direct_per_week} direct hours per week.")
st.write(f"You need to complete an average of {average_indirect_per_week} indirect hours per week.")

# User Input for Tracking Weekly Progress
st.header("Track Weekly Progress")
current_week = st.number_input("Select Week to Update", min_value=1, max_value=weeks_remaining, value=1)
week_date = start_date + datetime.timedelta(weeks=current_week - 1)
with st.expander(f"📅 Week {current_week} ({week_date.strftime('%B %d, %Y')})", expanded=True):
    st.markdown(f"<div style='background-color:#f0f0f5; padding:10px; border-radius:5px;'>", unsafe_allow_html=True)
    direct_hours = st.number_input(f"Direct Hours for Week {current_week}", min_value=0, value=st.session_state.weekly_direct_hours[current_week - 1], key=f"direct_{current_week}")
    indirect_hours = st.number_input(f"Indirect Hours for Week {current_week}", min_value=0, value=st.session_state.weekly_indirect_hours[current_week - 1], key=f"indirect_{current_week}")
    
    # Update session state with new values
    st.session_state.weekly_direct_hours[current_week - 1] = direct_hours
    st.session_state.weekly_indirect_hours[current_week - 1] = indirect_hours
    
    st.markdown(f"</div>", unsafe_allow_html=True)

# Weekly Progress Summary
st.header("Weekly Progress Summary")
progress_data = {
    "Week": [f"Week {i} ({(start_date + datetime.timedelta(weeks=i-1)).strftime('%B %d, %Y')})" for i in range(1, weeks_remaining + 1)],
    "Direct Hours": st.session_state.weekly_direct_hours,
    "Indirect Hours": st.session_state.weekly_indirect_hours
}
progress_df = pd.DataFrame(progress_data)
st.dataframe(progress_df)

# Visualize Weekly Progress in Charts
st.header("Weekly Progress Visualization")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(progress_data['Week'], progress_data['Direct Hours'], label='Direct Hours', marker='o', color='#007AFF')
ax.plot(progress_data['Week'], progress_data['Indirect Hours'], label='Indirect Hours', marker='o', color='#34C759')
ax.set_xlabel('Week', fontsize=10)
ax.set_ylabel('Hours', fontsize=10)
ax.set_title('Weekly Progress of Direct and Indirect Hours', fontsize=12)
ax.legend(title='Legend', fontsize=8)
st.pyplot(fig)

# Goal Progress Chart
st.header("Goal Progress Visualization")
fig_goal, ax_goal = plt.subplots(figsize=(10, 6))
ax_goal.bar(['Direct Hours Completed', 'Direct Hours Goal'], [sum(st.session_state.weekly_direct_hours), total_direct_hours_required], color='#007AFF', label='Direct Hours')
ax_goal.bar(['Indirect Hours Completed', 'Indirect Hours Goal'], [sum(st.session_state.weekly_indirect_hours), total_indirect_hours_required], color='#34C759', label='Indirect Hours')
ax_goal.set_ylabel('Hours', fontsize=10)
ax_goal.set_title('Total Progress Towards Goals', fontsize=12)
ax_goal.legend(title='Legend', fontsize=8)
st.pyplot(fig_goal)

# Goal Progress with Gauge Chart
st.header("Goal Progress Gauge Chart")
fig_gauge = go.Figure()
fig_gauge.add_trace(go.Indicator(
    mode="gauge+number",
    value=sum(st.session_state.weekly_direct_hours),
    title={'text': "Direct Hours Completed"},
    gauge={'axis': {'range': [0, total_direct_hours_required]}, 'bar': {'color': "#007AFF"}}
))
fig_gauge.add_trace(go.Indicator(
    mode="gauge+number",
    value=sum(st.session_state.weekly_indirect_hours),
    title={'text': "Indirect Hours Completed"},
    gauge={'axis': {'range': [0, total_indirect_hours_required]}, 'bar': {'color': "#34C759"}}
))
st.plotly_chart(fig_gauge, use_container_width=True)

# Calculate Total Hours
st.header("Summary")
total_direct_hours = direct_hours_completed + sum(st.session_state.weekly_direct_hours)
total_indirect_hours = indirect_hours_completed + sum(st.session_state.weekly_indirect_hours)

st.write(f"Total Direct Hours Completed: {total_direct_hours} / {total_direct_hours_required}")
st.write(f"Total Indirect Hours Completed: {total_indirect_hours} / {total_indirect_hours_required}")

# Play motivational audio if milestones are reached
if total_direct_hours >= total_direct_hours_required and total_indirect_hours >= total_indirect_hours_required:
    st.success("Congratulations! You have completed all required hours.")
    audio_file = open('congratulations.mp3', 'rb').read()
    play_audio(audio_file)
elif total_direct_hours >= total_direct_hours_required:
    st.info("You have completed all direct hours but still need to complete indirect hours.")
    audio_file = open('great_job.mp3', 'rb').read()
    play_audio(audio_file)
elif total_indirect_hours >= total_indirect_hours_required:
    st.info("You have completed all indirect hours but still need to complete direct hours.")
    audio_file = open('keep_going.mp3', 'rb').read()
    play_audio(audio_file)
else:
    st.warning("You still need to complete both direct and indirect hours.")

# Share Weekly Summary by Email or Text
st.header("Share Weekly Summary")
recipient_email = st.text_input("Enter recipient email address")
phone_number = st.text_input("Enter phone number (for SMS, optional)")

if st.button("Share Summary"):
    # Generate weekly summary text
    summary_text = f"Weekly Progress Summary:\n\nTotal Direct Hours Completed: {total_direct_hours} / {total_direct_hours_required}\nTotal Indirect Hours Completed: {total_indirect_hours} / {total_indirect_hours_required}"
    
    # Send email
    if recipient_email:
        try:
            sender_email = "your_email@example.com"
            sender_password = "your_password"
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = "Weekly Progress Summary"
            message.attach(MIMEText(summary_text, 'plain'))
            
            # Connect to SMTP server and send email
            server = smtplib.SMTP('smtp.example.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            server.quit()
            
            st.success(f"Summary sent successfully to {recipient_email}")
        except Exception as e:
            st.error(f"Failed to send email: {e}")
