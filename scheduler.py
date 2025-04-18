import time
import os
import streamlit as st
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from jobs import time_based, event_based

#Function to listen for manual event input from the terminal
def event_listener():
    """Continuously listens for user input on the terminal.
    If user types an event command, it triggers an event-based job in a new thread.
    Type 'quit' to stop the listener """
    while True:
        event = input("Enter event (or 'quit' to exit event listener): ")
        if event.lower() == 'quit':
            break
        # If the event starts with "click", treat it as a click event.
        if event.lower().startswith("click"):
            threading.Thread(target=event_based.run_click_event, args=(event,), daemon=True).start()
        else:
            threading.Thread(target=event_based.run_event_job, args=(event,), daemon=True).start()

def main():
    #Create an instance of the BackgroundScheduler.
    scheduler = BackgroundScheduler()

    """Schedule time-based jobs with various triggers. 
    Interval trigger for jobs that you want to run every x minutes, hours, etc. 
    Cron trigger for jobs that you want to run at a specified date/time interval ex: Run every Monday at 2AM or run everyday at 4:30AM"""
    scheduler.add_job(time_based.run_system_monitor, 'interval', minutes=5, id='run_system_monitor')
    scheduler.add_job(time_based.daily_log_rotation, 'cron', hour=0, minute=0, id='daily_log_rotation')
    scheduler.add_job(time_based.automated_backup, 'cron', hour=1, id='automated_backup')
    scheduler.add_job(time_based.update_check, 'cron', day_of_week='mon', hour=2, minute=0, id='update_check')
    scheduler.add_job(time_based.security_scan, 'cron', day_of_week='sun', hour=3, minute=0, id='security_scan')
    scheduler.add_job(time_based.clean_temp, 'interval', hours=1, id='clean_temp')
    scheduler.add_job(time_based.send_status_report, 'interval', minutes=30, id='send_status_report')
    scheduler.add_job(time_based.db_cleanup, 'cron', hour=4, minute=30, id='db_cleanup')
    scheduler.add_job(time_based.ping_test, 'interval', minutes=5, id='ping_test')
    scheduler.add_job(time_based.log_disk_usage, 'interval', hours=1, id='log_disk_usage')
    scheduler.add_job(time_based.resource_usage_trend_logger, 'interval', minutes=10, id='resource_usage_trend_logger')
    scheduler.add_job(time_based.memory_leak_detector, 'interval', minutes=2, id='memory_leak_detector')
    scheduler.add_job(time_based.log_file_analysis, 'cron', hour=5, minute=15, id='log_file_analysis')
    scheduler.add_job(time_based.service_health_check, 'interval', minutes=4, id='service_health_check')
    scheduler.add_job(time_based.temperature_monitoring, 'interval', minutes=15, id='temperature_monitoring')
    scheduler.add_job(time_based.force_error, trigger='interval', seconds=30, id='force_error_job')

    #Start scheduler so jobs can begin executing.
    scheduler.start()
    print("Scheduler started with time-based jobs.")

    # -------------------------------
    # Start Event-Based Threads (only once)
    # -------------------------------

    # 1. Start file watcher thread that monitors file system events
    if not hasattr(main, "threads_started"):
        #File watcher
        watcher_thread = threading.Thread(
            target = event_based.start_file_watcher,
            args = ("watched_directory",),
            daemon = True
        )
        watcher_thread.start()

    # 2. Start a thread to poll directory changes using os.listdir
    dir_poll_thread = threading.Thread(
        target=event_based.poll_directory_changes,
        args=("watched_directory", 10),  # (directory, polling interval in seconds)
        daemon=True
    )
    dir_poll_thread.start()

    # 3. Start a thread to poll file attribute changes for a specific file using os.stat
    file_poll_thread = threading.Thread(
        target=event_based.poll_file_attribute_changes,
        args=("/home/mozelle/cron_project/watched_directory/permanent.txt", 10),  # (file path, polling interval)
        daemon=True
    )
    file_poll_thread.start()

    # 4. Start a thread to poll disk space on the root mount using os.statvfs
    disk_poll_thread = threading.Thread(
        target=event_based.poll_disk_space,
        args=("/", 10, 30),  # (mount point, threshold percentage, polling interval)
        daemon=True
    )
    disk_poll_thread.start()

    # 5. Start a thread to poll environment variable changes
    env_poll_thread = threading.Thread(
        target=event_based.poll_env_variable_change,
        args=("MY_VAR", 10),  # (environment variable name, polling interval)
        daemon=True
    )
    env_poll_thread.start()
    print("All event-based threads have been started.")

    # -------------------------------
    # Start Manual Event Listener
    # -------------------------------
    try:
        event_listener() #Runs manual event input listener
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown() #Cleanly shutdown the scheduler on exit
        print("Scheduler shutdown.")


if __name__ == "__main__":
    main()
