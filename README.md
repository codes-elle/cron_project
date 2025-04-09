# Cron Project

**Cron Project** is a Python-based scheduler that mimics the functionality of the classic Unix/Linux cron daemon. It supports both time-based scheduling (using APScheduler) and event-based triggers (using watchdog and os polling), and it provides real-time statistical monitoring with live dashboards built using both Flask and Streamlit.

## Table of Contents

- [Features](#features)
- [System Architecture & Technologies](#system-architecture--technologies)
- [Quantitative Measurements and Analyses](#quantitative-measurements-and-analyses)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Project](#running-the-project)
  - [A. Running the Scheduler](#a-running-the-scheduler)
  - [B. Running the Live Dashboard](#b-running-the-live-dashboard)
- [Running as a Background Service](#running-as-a-background-service)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Time-Based Tasks:**  
  Schedule tasks using cron-like expressions or fixed intervals. The project leverages APScheduler to manage these tasks.
  
- **Event-Based Triggers:**  
  React to file system changes (using watchdog) and poll directories, file attributes, disk space, and environment variables using Python's os module.
  
- **Logging & Rotation:**  
  Uses Python's logging module with a `RotatingFileHandler` to automatically rotate and archive logs (stored in `job_logs.log`).

- **Runtime Statistics:**  
  Tracks key metrics (e.g., total runs, success vs. failure, execution duration, error counts) which are stored in a `stats.json` file in the project root.

- **Live Dashboards:**  
  Visualize key metrics via a Flask-based dashboard or a Streamlit-based live dashboard that displays multiple charts (bar, pie, etc.) in a grid layout.

- **Concurrent Execution:**  
  Implements multi-threading for both time-based and event-based tasks, ensuring that scheduled and event-triggered jobs run concurrently.

## System Architecture & Technologies

### Hardware
- **Target Environment:**  
  Designed to run on Unix/Linux systems (e.g., Ubuntu), suitable for servers, desktops, or virtual machines.

### Software Libraries / APIs
- **APScheduler:** For scheduling time-based tasks with cron-like and interval triggers.
- **Watchdog:** For monitoring file system events in real-time.
- **psutil:** For retrieving system resource usage (CPU, memory, disk, sensors).
- **Flask:** For creating a simple web-based dashboard.
- **Streamlit:** For building a live, interactive dashboard with real-time updating charts.
- **Plotly:** For generating interactive charts and graphs used in the Streamlit dashboard.
- **Python Logging Module:** For recording job execution details with automatic log rotation.

### Programming Languages / Platforms
- **Language:** Python 3.x
- **Platforms:** Developed and tested on Ubuntu Linux; runs as a command-line tool, service, or within containers.

### Algorithms & System Design
- **Scheduling:**  
  Time-based jobs are scheduled using APScheduler’s cron and interval methods, which closely mimic crontab behavior.
  
- **Event Detection:**  
  Event-based triggers are implemented using both:
  - Real-time file system monitoring (via Watchdog)
  - Periodic polling (using the os module functions such as os.listdir, os.stat, os.statvfs, os.environ)
  
- **Concurrency:**  
  Python threading enables simultaneous execution of multiple jobs.
  
- **Statistics & Logging:**  
  Execution metrics are recorded in a JSON file. The logging is managed by a rotating file handler, ensuring that logs remain at a manageable size.
  
- **Dashboard Integration:**  
  Live dashboards (both Flask and Streamlit) retrieve and display these metrics in real time using charts and tables for immediate insight.

## Quantitative Measurements and Analyses

The project tracks and analyzes a range of metrics, including:

1. **Total Runs per Job:**  
   The total number of times each job has been executed.

2. **Success vs. Failure Rates:**  
   The number of successful runs versus errors.

3. **Execution Duration:**  
   The average (and optionally minimum/maximum) execution time per job.

4. **Resource Usage:**  
   Live measurements of CPU, memory, and disk usage during job execution.

5. **Frequency of Occurrence:**  
   How often each job runs (e.g., per minute, hour, day).

6. **Error Trends:**  
   The frequency and type of errors encountered during execution.

7. **Job Category Totals:**  
   Aggregated run counts for time-based jobs compared to event-based jobs.

8. **Event-Specific Metrics:**  
   Detailed counts of particular events (file created, file modified, file deleted, file moved, etc.).

9. **Downtime/Recovery Rates:**  
   Metrics on job restarts or how often jobs recover from failures.

10. **Statistical Analyses:**  
    Additional statistical computations such as standard deviation, trend analysis, and performance metrics.

## Project Structure

```
cron_project/
├── dashboard/
│   ├── __init__.py
│   ├── app.py                # Flask-based dashboard (optional)
│   └── templates/
│       └── dashboard.html    # HTML template for the Flask dashboard
├── dashboard_streamlit.py    # Streamlit live dashboard
├── jobs/
│   ├── __init__.py
│   ├── time_based.py         # Time-based job definitions
│   └── event_based.py        # Event-based job definitions & polling functions
├── job_logger.py             # Logging configuration with RotatingFileHandler
├── scheduler.py              # Main scheduler that starts all jobs and event-based threads
├── rollback_scheduler.py     # Placeholder for rollback scheduling functionality
├── stats.py                  # Manages runtime statistics stored in stats.json
└── requirements.txt          # Python dependencies
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/codes-elle/cron_project.git
   cd cron_project
   ```

2. **Activate Your Virtual Environment:**

   If you’re using a virtual environment (e.g., `.venv`):

   ```bash
   source .venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Statistics File:**

   Run this once to create a fresh `stats.json` in the project root:

   ```bash
   python -c "from stats import initialize_stats; initialize_stats()"
   ```

5. **Prepare the Watched Directory:**

   Create the directory used for file system event monitoring:

   ```bash
   mkdir -p watched_directory
   ```

## Running the Project

### A. Run the Scheduler

The scheduler launches time-based jobs (using APScheduler) and starts event-based threads (for file system monitoring and polling).

```bash
python scheduler.py
```

This command starts the scheduler and prints log messages as tasks and event-based functions execute.

### B. Run the Live Dashboard

You have two options:

#### Option 1: Flask-Based Dashboard

1. **Navigate to the Dashboard Directory:**

   ```bash
   cd dashboard
   ```

2. **Run the Flask App:**

   ```bash
   python app.py
   ```

3. **Access the Dashboard:**

   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

#### Option 2: Streamlit Dashboard

1. **From the Project Root, Run:**

   ```bash
   streamlit run dashboard_streamlit.py
   ```

2. **Access the Dashboard:**

   Open [http://localhost:8501](http://localhost:8501) in your browser.

## Running as a Background Service

To run your tasks continuously even after closing your terminal, you can:
- **Create a systemd service:** Write a unit file to launch your scheduler on boot.
- **Use nohup or tmux/screen:** Run the scheduler in the background.
- **Containerize with Docker:** Run your application in detached mode.

## Contributing

Contributions, improvements, and bug fixes are welcome!  
Please open issues or submit pull requests to discuss changes.

## License

```

