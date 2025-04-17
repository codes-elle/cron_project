import streamlit as st
import pandas as pd
import json
import networkx as nx
#import time
import plotly.express as px
import psutil
from streamlit_autorefresh import st_autorefresh

#Caching, Streamlit avoids recomputing graph layout on each rerun
@st.cache_data(ttl=60)
def build_interaction_graph():
    G = nx.DiGraph()
    G.add_edges_from([
        ("scheduler.py", "jobs/time_based.py"),
        ("scheduler.py", "jobs/event_based.py"),
        ("jobs/time_based.py", "job_logger.py"),
        ("jobs/event_based.py", "job_logger.py"),
        ("job_logger.py", "stats.py"),
        ("stats.py", "dashboard_streamlit.py")
    ])
    pos = nx.spring_layout(G, seed=42)
    return G, pos

st.set_page_config(layout="wide")

# Automatically refresh the app every 30 seconds
st_autorefresh(interval=30000, limit=100, key="dashboard_refresh")


def load_stats():
    """Load the statistics from the stats.json file."""
    try:
        with open('stats.json', 'r') as f:
            stats = json.load(f)
    except Exception as e:
        stats = {}
    return stats


st.title("Live Scheduler Dashboard")
st.markdown("""
This dashboard displays key quantitative metrics and analyses for the scheduler project.

**Quantitative Measurements & Analyses:**
1. **Total Runs per Job:** Number of times each job is executed.
2. **Success vs. Failure Rates:** Successful executions versus errors.
3. **Execution Duration:** Average duration per job.
4. **Error Trends:** Number of errors per job.
5. **Job Category Totals:** Aggregated totals for Time-Based vs. Event-Based jobs.
6. **Resource Usage:** Current CPU, Memory, and Disk usage.
7. **Event-Specific Metrics:** Counts for file creation, modification, deletion, and moves.
8. **Statistical Summary:** A table of key metrics for each job.
""")

# Load stats from the JSON file
stats = load_stats()

# Initialize aggregated variables
time_success = 0
time_fail = 0
event_success = 0
event_fail = 0
time_total = 0
event_total = 0

# Prepare lists for per-job metrics
job_names = []
job_runs = []
job_errors = []
job_avg_duration = []

# Also, aggregate file event metrics
file_created = stats.get("file_created", {}).get("runs", 0)
file_modified = stats.get("file_modified", {}).get("runs", 0)
file_deleted = stats.get("file_deleted", {}).get("runs", 0)
file_moved = stats.get("file_moved", {}).get("runs", 0)

# Process each job's stats
for key, value in stats.items():
    runs = value.get('runs', 0)
    errors = value.get('errors', 0)
    total_duration = value.get('total_duration', 0.0)
    avg_duration = total_duration / runs if runs > 0 else 0
    job_names.append(key)
    job_runs.append(runs)
    job_errors.append(errors)
    job_avg_duration.append(avg_duration)

    # Classify by job type: assume keys starting with "time_based" are time-based; others are event-based.
    if key.startswith("time_based"):
        time_success += (runs - errors)
        time_fail += errors
        time_total += runs
    else:
        event_success += (runs - errors)
        event_fail += errors
        event_total += runs

# Chart 1: Bar Chart for Success vs. Failure Counts (aggregated)
df_bar = pd.DataFrame({
    'Job Category': ['Time-Based Successful', 'Time-Based Unsuccessful',
                     'Event-Based Successful', 'Event-Based Unsuccessful'],
    'Count': [time_success, time_fail, event_success, event_fail]
})

bar_fig = px.bar(
    df_bar,
    x='Job Category',
    y='Count',
    text='Count',
    color='Job Category',
    title="Job Success vs. Failure Counts"
)
bar_fig.update_layout(xaxis_title="Job Category", yaxis_title="Count")

# Chart 2: Pie Chart for Job Category Distribution
df_pie = pd.DataFrame({
    'Job Category': ['Time-Based Jobs', 'Event-Based Jobs'],
    'Count': [time_total, event_total]
})
pie_fig = px.pie(
    df_pie,
    values='Count',
    names='Job Category',
    title="Job Category Distribution (%)"
)

# Chart 3: Bar Chart for Average Execution Duration per Job
df_duration = pd.DataFrame({
    'Job': job_names,
    'Avg Duration (s)': job_avg_duration
})
duration_fig = px.bar(
    df_duration,
    x='Job',
    y='Avg Duration (s)',
    text='Avg Duration (s)',
    color='Job',
    title="Average Execution Duration per Job (seconds)"
)
duration_fig.update_layout(xaxis_title="Job", yaxis_title="Avg Duration (s)")

# Chart 4: Bar Chart for Error Counts per Job
df_errors = pd.DataFrame({
    'Job': job_names,
    'Error Count': job_errors
})
error_fig = px.bar(
    df_errors,
    x='Job',
    y='Error Count',
    text='Error Count',
    color='Job',
    title="Error Counts per Job"
)
error_fig.update_layout(xaxis_title="Job", yaxis_title="Error Count")

# Chart 5: Bar Chart for Total Runs per Job
df_runs = pd.DataFrame({
    'Job': job_names,
    'Total Runs': job_runs
})
runs_fig = px.bar(
    df_runs,
    x='Job',
    y='Total Runs',
    text='Total Runs',
    color='Job',
    title="Total Runs per Job"
)
runs_fig.update_layout(xaxis_title="Job", yaxis_title="Total Runs")

# Chart 6: Live Resource Usage (using psutil)
cpu_usage = psutil.cpu_percent(interval=0.5)
memory_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage('/').percent
df_resource = pd.DataFrame({
    'Resource': ['CPU Usage', 'Memory Usage', 'Disk Usage'],
    'Usage (%)': [cpu_usage, memory_usage, disk_usage]
})
resource_fig = px.bar(
    df_resource,
    x='Resource',
    y='Usage (%)',
    text='Usage (%)',
    color='Resource',
    title="Current Resource Usage (%)"
)
resource_fig.update_layout(xaxis_title="Resource", yaxis_title="Usage (%)")

# Chart 7: Bar Chart for File Event Metrics
df_file_events = pd.DataFrame({
    'Event Type': ['File Created', 'File Modified', 'File Deleted', 'File Moved'],
    'Count': [file_created, file_modified, file_deleted, file_moved]
})
file_event_fig = px.bar(
    df_file_events,
    x='Event Type',
    y='Count',
    text='Count',
    color='Event Type',
    title="File Event Metrics"
)
file_event_fig.update_layout(xaxis_title="File Event Type", yaxis_title="Count")

# Chart 8: Data Table for Per-Job Metrics
df_summary = pd.DataFrame({
    'Job': job_names,
    'Total Runs': job_runs,
    'Errors': job_errors,
    'Avg Duration (s)': job_avg_duration
})

# Arrange charts in grid: two per row

st.markdown("## Job Success vs. Failure & Category Distribution")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_fig, use_container_width=True)
with col2:
    st.plotly_chart(pie_fig, use_container_width=True)

st.markdown("## Execution Duration & Error Counts per Job")
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(duration_fig, use_container_width=True)
with col4:
    st.plotly_chart(error_fig, use_container_width=True)

st.markdown("## Total Runs per Job & Resource Usage")
col5, col6 = st.columns(2)
with col5:
    st.plotly_chart(runs_fig, use_container_width=True)
with col6:
    st.plotly_chart(resource_fig, use_container_width=True)

st.markdown("## File Event Metrics")
st.plotly_chart(file_event_fig, use_container_width=True)

st.markdown("## Summary Table of Job Metrics")
st.dataframe(df_summary)
