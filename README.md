# Cron Project

**Cron Project** is a robust Python-based scheduler that extends the functionality of the traditional Unix/Linux cron daemon. It supports both time-based scheduling via APScheduler and event-driven triggers (using Watchdog and os polling). Additionally, it records execution metrics in a centralized `stats.json` file and provides real-time, interactive visualizations through a Streamlit dashboard.

---

## Table of Contents

- [Features](#features)
- [System Architecture & Technologies](#system-architecture--technologies)
- [Quantitative Measurements and Analyses](#quantitative-measurements-and-analyses)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Project](#running-the-project)
  - [Scheduler & Jobs](#scheduler--jobs)
  - [Live Dashboard](#live-dashboard)
  - [Background Service Options](#background-service-options)
- [Updates and Improvements](#updates-and-improvements)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Time-Based Tasks:**  
  Schedule tasks with cron-like expressions and fixed intervals using APScheduler.
- **Event-Based Triggers:**  
  React to file system events with Watchdog and monitor directories, file attributes, disk space, and environment variables using polling functions.
- **Logging & Log Rotation:**  
  A robust logging system uses TimedRotatingFileHandler to automatically archive logs (stored in `job_logs.log`) daily.
- **Runtime Statistics:**  
  Each job logs key metrics—run counts, execution durations, and error counts—to a single `stats.json` file.
- **Live Dashboard:**  
  An interactive Streamlit dashboard displays real-time performance data with multiple charts arranged in a grid layout.
- **Concurrency:**  
  Using Python threading, both time-based and event-driven tasks run concurrently.
- **Extensibility:**  
  The modular design allows for easy integration of future features like priority scheduling or distributed job coordination.

---

## System Architecture & Technologies

### Hardware

- **Target Environment:**  
  Designed to run on Unix/Linux systems (e.g., Ubuntu), suitable for desktops, servers, or virtual machines.

### Software Libraries / APIs

- **APScheduler:** Manages time-based task scheduling.
- **Watchdog:** Monitors file system events in real time.
- **psutil:** Retrieves system metrics (CPU, memory, disk usage, etc.).
- **Streamlit & Plotly:** Create interactive, real-time dashboards.
- **Python Logging Module:** Configured with TimedRotatingFileHandler for automatic log rotation.
  
### Programming Languages / Platforms

- **Language:** Python 3.x  
- **Platform:** Developed and tested on Ubuntu Linux.
- **Execution:** The project can run as a standalone script or background service, and it can be containerized via Docker for production.

### System Design

The project consists of:
- A scheduler that integrates both time-based and event-driven tasks.
- A statistics system that aggregates performance data into `stats.json`.
- A logging system that archives logs daily.
- A live dashboard (using Streamlit) that displays key performance metrics and analyses.

---

## Quantitative Measurements and Analyses

The project tracks numerous performance metrics:
1. **Total Runs per Job:** Overall execution counts.
2. **Success vs. Failure Rates:** The ratio of successful runs to errors.
3. **Execution Duration:** Average, minimum, and maximum runtime for each job.
4. **Resource Usage:** Live metrics of CPU, memory, and disk usage.
5. **Frequency of Execution:** How often each job is executed.
6. **Error Trends:** Number and types of errors per job.
7. **Job Category Totals:** Aggregated metrics for time-based vs. event-based tasks.
8. **Event-Specific Metrics:** Counts of specific file events (creation, modification, deletion, moves).
9. **Downtime/Recovery Rates:** Frequency of job restarts or recoveries.
10. **Statistical Analysis:** Derived metrics such as standard deviations and trends over time.

These metrics are used to generate detailed visualizations in the live dashboard.

---

## Project Structure

```
cron_project/
├── dashboard_streamlit.py    # Streamlit live dashboard for interactive visualization
├── jobs/
│   ├── __init__.py
│   ├── time_based.py         # Definitions of time-based jobs
│   └── event_based.py        # Definitions of event-based jobs & polling functions
├── job_logger.py             # Logging configuration with TimedRotatingFileHandler
├── scheduler.py              # Main scheduler that launches all tasks and threads
├── rollback_scheduler.py     # Optional; placeholder for rollback functionality
├── stats.py                  # Manages runtime statistics stored in stats.json
└── requirements.txt          # List of Python dependencies
```

*Note: The Flask dashboard has been removed, so only the Streamlit dashboard is used.*

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/codes-elle/cron_project.git
   cd cron_project
   ```
2. **Activate Your Virtual Environment:**
   ```bash
   source .venv/bin/activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Initialize the Statistics File:**
   Run once to create a fresh `stats.json` in the project root:
   ```bash
   python -c "from stats import initialize_stats; initialize_stats()"
   ```
5. **Prepare the Watched Directory:**
   ```bash
   mkdir -p watched_directory
   ```

---

## Running the Project

### Scheduler & Jobs

To start the scheduler—which initiates time-based jobs via APScheduler and launches event-based threads (file watcher, polling functions, and manual event listener)—run:
```bash
python scheduler.py
```
This command will output log messages and update job metrics in `stats.json` while running concurrently.

### Live Dashboard

#### Streamlit Dashboard

From the project root, run:
```bash
streamlit run dashboard_streamlit.py
```
Then, open your browser and visit [http://localhost:8501](http://localhost:8501) to view the live, interactive dashboard with charts and tables that visualize your project’s metrics.

### Background Service Options

To ensure that your time-based tasks continue running after you close your terminal:
- **Systemd Service:**  
  Create a systemd unit file for `scheduler.py` so that it starts on system boot.
- **Tmux/Screen/Nohup:**  
  Run `scheduler.py` in a detached session using `tmux`, `screen`, or `nohup`.
- **Docker:**  
  Containerize your project and run it in detached mode for production deployment.

---

## Updates and Improvements

Recent improvements include:
- **Consolidated Statistics:**  
  Duplicate keys have been merged in `stats.json`, ensuring each measurement is tracked only once.
- **Enhanced Log Rotation:**  
  The logging system uses TimedRotatingFileHandler to rotate logs daily.
- **Path Configuration:**  
  Absolute paths have been replaced with relative paths (using `os.path.join(os.getcwd(), ...)`) for improved portability.
- **Dashboard Upgrades:**  
  The project now includes a fully featured Streamlit dashboard that displays all key quantitative measurements in an interactive grid layout.
- **Optimized Concurrency:**  
  Time-based and event-based tasks run in separate threads for higher performance and reliability.

---

## Contributing

Contributions, feature requests, and bug fixes are welcome! Please fork the repository and submit pull requests, or open issues to discuss changes.

---

## License

[Include your license information here.]

---
