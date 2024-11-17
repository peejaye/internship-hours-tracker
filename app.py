import streamlit as st
import pandas as pd

# Initialize data
weeks_remaining = 14
data = {
    "Week": [f"Week {i+1}" for i in range(weeks_remaining)],
    "Direct Hours Needed (Min)": [10] * weeks_remaining,
    "Direct Hours Needed (Avg)": [10] * weeks_remaining,
    "Indirect Hours Needed (Min)": [6] * weeks_remaining,
    "Indirect Hours Needed (Avg)": [6] * weeks_remaining,
    "Direct Hours Intended": [0] * weeks_remaining,
    "Indirect Hours Intended": [0] * weeks_remaining,
    "Direct Hours Actual": [0] * weeks_remaining,
    "Indirect Hours Actual": [0] * weeks_remaining,
}
df = pd.DataFrame(data)

# Streamlit app
st.title("Internship Hours Tracker")

# Editable table
st.subheader("Weekly Data")
edited_df = st.data_editor(df, num_rows="dynamic")

# Calculations
edited_df["Total Direct Hours Achieved"] = edited_df["Direct Hours Actual"].cumsum()
edited_df["Total Indirect Hours Achieved"] = edited_df["Indirect Hours Actual"].cumsum()
edited_df["Grand Total Direct Remaining"] = 260 - 119 - edited_df["Total Direct Hours Achieved"]
edited_df["Grand Total Indirect Remaining"] = 600 - 512 - edited_df["Total Indirect Hours Achieved"]

# Display updated table
st.subheader("Updated Table with Totals")
st.dataframe(edited_df)

# Downloadable file
@st.cache_data
def convert_df(df):
    return df.to_excel(index=False)

st.download_button(
    label="Download Excel File",
    data=convert_df(edited_df),
    file_name="Internship_Hours_Tracker.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

