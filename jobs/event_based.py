import datetime
import time
import os
import subprocess
import shutil
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from stats import update_stat
from job_logger import log_job

# 1. Generic Event Trigger
@log_job("Generic Event", "Handle a generic event", file_type="N/A")
def run_event_job(event):
    print(f"[{datetime.datetime.now()}] Running event-based job for event: {event}")
    update_stat("event_based_generic")

# 2. Click Event
@log_job("Click Event", "Handle a simulated click event", file_type="N/A")
def run_click_event(click_info):
    print(f"[{datetime.datetime.now()}] Click event detected: {click_info}")
    update_stat("event_based_click")

# 3. File Created Event
@log_job("File Created Event", "Handle file creation event", file_type="File")
def file_created_event(event):
    print(f"[{datetime.datetime.now()}] File created: {event.src_path}")
    update_stat("file_created")

# 4. File Modified Event
@log_job("File Modified Event", "Handle file modification event", file_type="File")
def file_modified_event(event):
    print(f"[{datetime.datetime.now()}] File modified: {event.src_path}")
    update_stat("file_modified")

# 5. File Deleted Event
@log_job("File Deleted Event", "Handle file deletion event", file_type="File")
def file_deleted_event(event):
    print(f"[{datetime.datetime.now()}] File deleted: {event.src_path}")
    update_stat("file_deleted")

# 6. File Moved Event
@log_job("File Moved Event", "Handle file moved event", file_type="File")
def file_moved_event(event):
    print(f"[{datetime.datetime.now()}] File moved: from {event.src_path} to {event.dest_path}")
    update_stat("file_moved")

# 7. Configuration Change Alert
@log_job("Config Change Alert", "Alert on critical configuration file change", file_type="Config")
def config_change_alert(event):
    # Update the path as needed
    if event.src_path == '/etc/ssh/ssh_config':
        print("SSH configuration file has changed!")
        update_stat("event_based_config_change")

# 8. Monitor USB Insertion
@log_job("USB Insertion", "Handle USB device insertion event", file_type="USB")
def monitor_usb_insertion(event):
    print(f"[{datetime.datetime.now()}] USB device inserted: {event.device}")
    update_stat("event_based_usb_insertion")

# 9. Monitor USB Removal
@log_job("USB Removal", "Handle USB device removal event", file_type="USB")
def monitor_usb_removal(event):
    print(f"[{datetime.datetime.now()}] USB device removed: {event.device}")
    update_stat("event_based_usb_removal")

# 10. User Login/Logout Event
@log_job("User Login/Logout", "Handle user login/logout event", file_type="User")
def user_login_logout_event(event):
    print(f"[{datetime.datetime.now()}] User login/logout event: {event.detail}")
    update_stat("event_based_user_event")

# 11. Trigger File Handler
@log_job("Trigger File Handler", "Handle trigger file creation", file_type="File")
def trigger_file_handler(event):
    if event.src_path.endswith("trigger.txt"):
        print("Trigger file detected—executing maintenance job.")
        update_stat("event_based_trigger_file")

# 12. Log Keyword Alert
@log_job("Keyword Alert", "Scan log file change for specific keyword", file_type="Log")
def log_keyword_alert(event, keyword="ERROR"):
    print(f"[{datetime.datetime.now()}] Log file change detected, checking for keyword: {keyword}")
    update_stat("event_based_keyword_alert")

# 13. Network Interface Change Event
@log_job("Network Interface Change", "Detect changes in network interface status", file_type="Network")
def network_interface_change_event(event):
    print(f"[{datetime.datetime.now()}] Network interface change detected: {event.detail}")
    update_stat("event_based_network_change")

# 14. Temperature Threshold Exceeded Event
@log_job("Temperature Threshold Exceeded", "Alert when sensor temperature exceeds threshold", file_type="Sensor")
def temperature_threshold_exceeded_event(event):
    print(f"[{datetime.datetime.now()}] Temperature threshold exceeded: {event.detail}")
    update_stat("event_based_temp_exceeded")

# 15. Low Disk Space Alert Event
@log_job("Low Disk Space Alert", "Alert when available disk space is low", file_type="Disk")
def low_disk_space_alert_event(event):
    print(f"[{datetime.datetime.now()}] Low disk space detected: {event.detail}")
    update_stat("event_based_disk_low")


# File System Event Handler using watchdog – calls some of the above functions
class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        file_created_event(event)
    def on_modified(self, event):
        file_modified_event(event)
        config_change_alert(event)
        log_keyword_alert(event)
    def on_deleted(self, event):
        file_deleted_event(event)
    def on_moved(self, event):
        file_moved_event(event)
        #Backup config on change
        backup_config_on_change(event)

def start_file_watcher(path_to_watch):
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path='watched_directory', recursive=True)
    observer.start()
    print(f"Started file watcher on {path_to_watch}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# Helper function used within the event handler for backing up configuration files
@log_job("Backup Config", "Backup configuration file on change", file_type="Config")
def backup_config_on_change(event):
    critical_files = ['/etc/ssh/ssh_config', '/etc/fstab']
    if event.src_path in critical_files:
        backup_path = event.src_path + ".backup"
        try:
            shutil.copy(event.src_path, backup_path)
            print(f"Backup created for {event.src_path}")
        except Exception as e:
            print(f"Failed to backup {event.src_path}: {e}")
        update_stat("event_based_config_backup")

#Polling functions using 'os' Module
@log_job("os_directory_change", "Detect changes in directory listing using os.listdir", file_type="Directory")
def poll_directory_changes(directory_path, interval=10):
    """
    Poll a directory for changes in its file listing.
    If files are added or removed, log the changes and update stats.
    """
    previous_listing = set(os.listdir(directory_path))
    while True:
        time.sleep(interval)
        current_listing = set(os.listdir(directory_path))
        added = current_listing - previous_listing
        removed = previous_listing - current_listing
        if added or removed:
            print(f"Directory changes in {directory_path}. Added: {added}, Removed: {removed}")
            update_stat("os_directory_change")
            previous_listing = current_listing

@log_job("os_file_attribute_change", "Monitor file attribute changes using os.stat", file_type="File")
def poll_file_attribute_changes(file_path, interval=10):
    """
    Poll a file for attribute changes (e.g., modification time, size).
    """
    try:
        previous_stat = os.stat(file_path)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        previous_stat = None

    while True:
        time.sleep(interval)
        try:
            current_stat = os.stat(file_path)
        except FileNotFoundError:
            current_stat = None
        if previous_stat and current_stat:
            if current_stat.st_mtime != previous_stat.st_mtime or current_stat.st_size != previous_stat.st_size:
                print(f"File attributes changed for {file_path}.")
                update_stat("os_file_attribute_change")
                previous_stat = current_stat
        elif previous_stat is None and current_stat is not None:
            print(f"File {file_path} appeared.")
            update_stat("os_file_attribute_change")
            previous_stat = current_stat
        elif previous_stat is not None and current_stat is None:
            print(f"File {file_path} is now missing.")
            update_stat("os_file_attribute_change")
            previous_stat = None

@log_job("os_disk_space", "Monitor disk space using os.statvfs", file_type="Disk")
def poll_disk_space(mount_point, threshold=10, interval=30):
    """
    Poll disk space on a given mount point.
    If free space drops below the threshold (percentage), trigger an event.
    """
    while True:
        time.sleep(interval)
        stats = os.statvfs(mount_point)
        total_space = stats.f_frsize * stats.f_blocks
        free_space = stats.f_frsize * stats.f_bavail
        free_percent = (free_space / total_space) * 100
        if free_percent < threshold:
            print(f"Low disk space alert on {mount_point}: {free_percent:.2f}% free")
            update_stat("os_disk_space")
        else:
            print(f"Disk space OK on {mount_point}: {free_percent:.2f}% free")

@log_job("os_env_change", "Monitor changes to an environment variable using os.environ", file_type="Env")
def poll_env_variable_change(var_name, interval=10):
    """
    Poll an environment variable for changes.
    """
    previous_value = os.environ.get(var_name)
    while True:
        time.sleep(interval)
        current_value = os.environ.get(var_name)
        if current_value != previous_value:
            print(f"Environment variable {var_name} changed from {previous_value} to {current_value}")
            update_stat("os_env_change")
            previous_value = current_value
