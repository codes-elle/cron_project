import json
import threading
import os

STATS_FILE = "stats.json"
lock = threading.Lock()


def initialize_stats():
    """Initialize the stats file if it does not exist."""
    if not os.path.exists("stats.json"):
        stats = {
            # Time-based jobs
            "time_based_system_monitor": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_log_rotation": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_backup": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_update_check": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_security_scan": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_clean_temp": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_status_report": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_db_cleanup": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_ping_test": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_log_disk_usage": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_resource_trend": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_memory_leak_detector": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_log_file_analysis": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_service_health_check": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "time_based_temperature_monitoring": {"runs": 0, "total_duration": 0.0, "errors": 0},

            # Event-based jobs
            "event_based_generic": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "event_based_click": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "file_created": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "file_modified": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "file_deleted": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "file_moved": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "event_based_config_change": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "event_based_usb_insertion": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "event_based_usb_removal": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "event_based_user_event": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "event_based_trigger_file": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "event_based_keyword_alert": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "event_based_config_backup": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "event_based_network_change": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "event_based_temp_exceeded": {"runs": 0, "total_duration": 0.0, "errors": 0},
            "event_based_disk_low": {"runs": 0, "total_duration": 0.0, "errors": 0}
        }
        with open(STATS_FILE, "w") as f:
            json.dump(stats, f)


def update_stat(job_type, duration=0.0, error=False):
    """
    Update statistics for a given job.

    Args:
        job_type (str): The key for the job in the stats structure.
        duration (float): The execution duration in seconds.
        error (bool): True if the job encountered an error.
    """
    with lock:
        try:
            with open(STATS_FILE, "r") as f:
                stats = json.load(f)
        except Exception as e:
            stats = {}
        if job_type in stats:
            stats[job_type]["runs"] += 1
            stats[job_type]["total_duration"] += duration
            if error:
                stats[job_type]["errors"] += 1
        else:
            stats[job_type] = {"runs": 1, "total_duration": duration, "errors": 1 if error else 0}
        with open(STATS_FILE, "w") as f:
            json.dump(stats, f)


def get_stats():
    """Return the current statistics."""
    with lock:
        if not os.path.exists(STATS_FILE):
            initialize_stats()
        with open(STATS_FILE, "r") as f:
            stats = json.load(f)
    return stats



if __name__ == "__main__":
    initialize_stats()
    print("Stats initialized.")
