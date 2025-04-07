import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from jobs import time_based, event_based

def event_listener():
    """Listen for event input and trigger event-based jobs."""
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
    scheduler = BackgroundScheduler()
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
    scheduler.start()

    # -------------------------------
    # Start Event-Based Threads
    # -------------------------------
    # 1. File watcher for filesystem events (using watchdog)
    watcher_thread = threading.Thread(
        target=event_based.start_file_watcher,
        args=("/home/mozelle/cron_project/watched_directory",),  # Update path as needed
        daemon=True
    )
    watcher_thread.start()

    # 2. Poll directory changes (using os.listdir)
    dir_poll_thread = threading.Thread(
        target=event_based.poll_directory_changes,
        args=("/home/mozelle/cron_project/watched_directory", 10),  # (directory, polling interval in seconds)
        daemon=True
    )
    dir_poll_thread.start()

    # 3. Poll file attribute changes (using os.stat)
    file_poll_thread = threading.Thread(
        target=event_based.poll_file_attribute_changes,
        args=("/home/mozelle/cron_project/watched_directory.permanent.txt", 10),  # (file path, polling interval)
        daemon=True
    )
    file_poll_thread.start()

    # 4. Poll disk space (using os.statvfs)
    disk_poll_thread = threading.Thread(
        target=event_based.poll_disk_space,
        args=("/", 10, 30),  # (mount point, threshold percentage, polling interval)
        daemon=True
    )
    disk_poll_thread.start()

    # 5. Poll environment variable changes
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
        event_listener()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()
        print("Scheduler shutdown.")


if __name__ == "__main__":
    main()
