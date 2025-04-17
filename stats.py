import json
import threading
import os

#The file where stats are stored. Will be created in project root
STATS_FILE = "stats.json"

#A lock to make sure file operations are thread-safe
lock = threading.Lock()


def initialize_stats():
    """Initialize the stats file if it does not exist.
    Function creates a baseline for all job metrics."""
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
    This function opens the stats.json file, updates the run count, duration,
    and increments the error count if error is True.

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
        #Update or create the key for the given job_type
        if job_type in stats:
            stats[job_type]["runs"] += 1
            stats[job_type]["total_duration"] += duration
            if error:
                stats[job_type]["errors"] += 1
        else:
            stats[job_type] = {"runs": 1, "total_duration": duration, "errors": 1 if error else 0}
        with open(STATS_FILE, "w") as f:
            json.dump(stats, f)

    def prune_stats(max_entries=500): #prevent infinite growth
        """ Keep only the most recent max_entries keys or timestamps """
        with lock:
            stats = json.load(open(STATS_FILE))
            if len(stats) > max_entries:
                # example: sort by timestamp key if you stored timestamps
                keys_to_keep = sorted(stats, key=lambda k: stats[k]['last_run_ts'], reverse=True)[:max_entries]
                stats = {k: stats[k] for k in keys_to_keep}
                with open(STATS_FILE, 'w') as f:
                    json.dump(stats, f)


def get_stats():
    """Return the current statistics from the stats.json file.
    If the file doesn't exist, it initializes it first"""
    with lock:
        if not os.path.exists(STATS_FILE):
            initialize_stats()
        with open(STATS_FILE, "r") as f:
            stats = json.load(f)
    return stats

if __name__ == "__main__":
    initialize_stats()
    print("Stats initialized.")
