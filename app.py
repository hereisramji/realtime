import streamlit as st
import pandas as pd
from models.schedule import SampleSchedule
from models.simulation import CytometrySimulation
from utils.visualization import create_population_plots, create_summary_table
from utils.constants import DEFAULT_SCHEDULE, DEFAULT_BATCH_SIZE, DEFAULT_REALTIME_CV

st.set_page_config(page_title="Cytometry Data Visualization", layout="wide")

st.title("Cytometry Data Visualization")
st.markdown("""
This application visualizes simulated cytometry data for various cell populations,
comparing Batch Mode and Real-Time Mode processing strategies. You can customize the sample
collection schedule and processing parameters using the sidebar controls.
""")

# Sidebar inputs
st.sidebar.header("Settings")

# Schedule input
st.sidebar.subheader("Sample Collection Schedule")
default_schedule_text = "\n".join(f"{date}: {count}" for date, count in DEFAULT_SCHEDULE)
schedule_text = st.sidebar.text_area(
    "Enter schedule (one entry per line, format: MM/DD/YYYY: count)",
    value=default_schedule_text,
    height=300
)

if st.sidebar.button("Reset to Default Schedule"):
    schedule_text = default_schedule_text

# Validate and parse schedule
schedule_data = SampleSchedule.validate_schedule_input(schedule_text)
if schedule_data is None:
    st.error("Invalid schedule format. Please check the input format and try again.")
    st.stop()

schedule = SampleSchedule(schedule_data)

# Batch size slider
batch_size = st.sidebar.slider(
    "Batch Size",
    min_value=20,
    max_value=schedule.total_samples,
    value=DEFAULT_BATCH_SIZE,
    help="Minimum number of samples required to trigger a batch run"
)

# Real-time CV input
realtime_cv = st.sidebar.number_input(
    "Real-Time Mode CV (%)",
    min_value=0.1,
    max_value=50.0,
    value=DEFAULT_REALTIME_CV,
    step=0.1,
    help="Overall coefficient of variation for real-time mode"
)

# Generate processing runs
batch_runs = schedule.get_batch_runs(batch_size)
realtime_runs = schedule.get_realtime_runs()

# Simulate data
simulator = CytometrySimulation(realtime_cv)
batch_results = simulator.simulate_batch_mode(batch_runs)
realtime_results = simulator.simulate_realtime_mode(realtime_runs)

# Create visualization
st.subheader("Cell Population Frequencies")
st.markdown("""
The plots below show simulated frequencies for each cell population in both processing modes.
Point sizes are proportional to the number of samples in each run. The red dashed line shows
the true value for each population.
""")
fig = create_population_plots(batch_runs, realtime_runs, batch_results, realtime_results)
st.pyplot(fig)

# Display summary statistics
st.subheader("Summary Statistics")
st.markdown("""
The table below shows summary statistics for each cell population and processing mode,
including mean values, deviation from true values, and coefficients of variation.
""")
summary_df = create_summary_table(batch_runs, realtime_runs, batch_results, realtime_results)
st.dataframe(summary_df, use_container_width=True)

# Display schedule information
st.sidebar.markdown("---")
st.sidebar.subheader("Schedule Summary")
st.sidebar.write(f"Total Samples: {schedule.total_samples}")
st.sidebar.write(f"Batch Mode Runs: {len(batch_runs)}")
st.sidebar.write(f"Real-Time Mode Runs: {len(realtime_runs)}")

# Add explanatory notes
st.markdown("---")
st.markdown("""
### Notes
- **Batch Mode**: Accumulates samples until reaching the specified batch size before processing
- **Real-Time Mode**: Processes samples immediately upon arrival
- **Point Sizes**: Larger points indicate more samples in that particular run
- **CV**: Coefficient of Variation, a measure of relative variability
""") 