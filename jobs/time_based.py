import time
import datetime
import os
import shutil
import subprocess
import psutil
from stats import update_stat
from job_logger import log_job

#----------------------
# Time-Based Job Functions
#----------------------

# 1. System Resource Monitor
@log_job("System Monitor", "Monitor CPU, memory, disk usage, and uptime")
def run_system_monitor():
    """
    Runs a system monitor that gathers CPU, memory, and disk usage.
    Calculates uptime. Updates starts after execution
    """
    now = datetime.datetime.now()
    cpu = psutil.cpu_percent(interval=1) #CPU usage over a 1 second interval
    memory = psutil.virtual_memory().percent #Memory usage percentage
    disk = psutil.disk_usage('/').percent  # Disk usage on the root filesystem. Change '/' if needed
    uptime_seconds = int(time.time() - psutil.boot_time()) #Calculates system uptime
    print(f"[{now}] System Monitor - CPU: {cpu}%, Memory: {memory}%, Disk: {disk}%, Uptime: {uptime_seconds} seconds")
    update_stat("time_based_system_monitor")

# 2. Daily Log Rotation
@log_job("Daily Log Rotation", "Rotate and archive logs older than 24 hours")
def daily_log_rotation():
    """
    Rotates logs by moving log files older than 24hrs from the log directory to an archive.
    Paths are relative to the project root.
    """
    log_dir = '/var/log/myapp/'       # Update to your log directory
    archive_dir = '/var/log/myapp/archive/'
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    now_ts = time.time()
    for file in os.listdir(log_dir):
        if file.endswith('.log'):
            path = os.path.join(log_dir, file)
            if os.path.getmtime(path) < now_ts - 86400:
                shutil.move(path, os.path.join(archive_dir, file))
                print(f"Rotated log file: {file}")
    update_stat("time_based_log_rotation")

# 3. Automated Backup
@log_job("Automated Backup", "Backup a critical directory as a ZIP archive")
def automated_backup():
    """
    Creates a backup of a critical directory by zipping it.
    Source and destination paths are relative to the project root.
    """
    source = 'important_data'   # Update to your source directory
    destination = '/backup/backup'  # Update to your backup destination
    shutil.make_archive(destination, 'zip', source)
    print("Automated backup completed.")
    update_stat("time_based_backup")

# 4. Update Check
@log_job("Update Check", "Run system package update check")
def update_check():
    """
    Runs a system package update check using apt-get
    Function is scheduled to run at a fixed time
    """
    print("Running update check...")
    subprocess.run(['sudo', 'apt-get', 'update'])
    update_stat("time_based_update_check")

# 5. Security Scan
@log_job("Security Scan", "Run a security scan using ClamAV")
def security_scan():
    """
    Runs a security scan using ClamAV over the root filesystem.
    Updates statistics after scanning.
    """
    print("Running security scan...")
    subprocess.run(['clamscan', '-r', '/'])
    update_stat("time_based_security_scan")

# 6. Clean Temporary Files
@log_job("Clean Temp", "Clean temporary files from /tmp")
def clean_temp():
    """
    Deletes files in the /tmp directory to free up disk space.
    """
    temp_dir = '/tmp'
    for file in os.listdir(temp_dir):
        try:
            os.remove(os.path.join(temp_dir, file))
        except Exception:
            pass
    print("Temporary files cleaned.")
    update_stat("time_based_clean_temp")

# 7. Send Status Report
@log_job("Status Report", "Generate and print a status report")
def send_status_report():
    """
    Creates a status report by printing the current timestamp and other relevant info
    """
    report = f"Status Report at {datetime.datetime.now()}"
    print(report)
    update_stat("time_based_status_report")

# 8. Database Cleanup
@log_job("Database Cleanup", "Perform database maintenance tasks")
def db_cleanup():
    """
    Placeholder for database maintenance operations such as vacuuming or cleanup
    """
    print("Database maintenance performed.")
    update_stat("time_based_db_cleanup")

# 9. Ping Test
@log_job("Ping Test", "Test network connectivity by pinging critical servers")
def ping_test():
    """
    Pings a set of critical servers to test network connectivity
    """
    for server in ['8.8.8.8', '8.8.4.4']:
        subprocess.run(['ping', '-c', '2', server])
    print("Network connectivity test completed.")
    update_stat("time_based_ping_test")

# 10. Log Disk Usage
@log_job("Log Disk Usage", "Append disk usage statistics to a log file")
def log_disk_usage():
    """
    Logs current disk usage to a local log file
    """
    disk = psutil.disk_usage('/').percent
    with open('disk_usage.log', 'a') as f:
        f.write(f"{time.ctime()}: Disk usage: {disk}%\n")
    print("Disk usage logged.")
    update_stat("time_based_log_disk_usage")

# 11. Resource Usage Trend Logger
@log_job("Resource Usage Trend Logger", "Log average CPU and memory usage over a period")
def resource_usage_trend_logger():
    """
    Collects CPU and memory usage readings and computes the average.
    """
    cpu_readings = []
    mem_readings = []
    for _ in range(5):
        cpu_readings.append(psutil.cpu_percent(interval=0.5))
        mem_readings.append(psutil.virtual_memory().percent)
    avg_cpu = sum(cpu_readings) / len(cpu_readings)
    avg_mem = sum(mem_readings) / len(mem_readings)
    print(f"Average CPU: {avg_cpu:.2f}%, Average Memory: {avg_mem:.2f}%")
    update_stat("time_based_resource_trend")

# 12. Memory Leak Detector
@log_job("Memory Leak Detector", "Detect if memory usage exceeds a threshold")
def memory_leak_detector():
    """
    Checks if memory usage exceeds a specific threshold (%). If it does, prints a warning.
    Useful for memory leaks.
    """
    threshold = 90  #Percentage threshold
    mem_usage = psutil.virtual_memory().percent
    if mem_usage > threshold:
        print(f"WARNING: Memory usage is high at {mem_usage}%!")
    else:
        print(f"Memory usage is normal at {mem_usage}%.")
    update_stat("time_based_memory_leak_detector")

# 13. Log File Analysis
@log_job("Log File Analysis", "Scan a log file for error patterns")
def log_file_analysis():
    """
    Reads a system log and counts lines with 'ERROR' or 'CRITICAL'
    """
    log_path = '/var/log/syslog'  # Adjust as needed
    error_count = 0
    try:
        with open(log_path, 'r') as f:
            for line in f:
                if "ERROR" in line or "CRITICAL" in line:
                    error_count += 1
    except Exception as e:
        print(f"Failed to analyze log file: {e}")
    print(f"Found {error_count} error entries in {log_path}.")
    update_stat("time_based_log_file_analysis")

# 14. Service Health Check
@log_job("Service Health Check", "Check if critical services are running")
def service_health_check():
    """
    Checks whether a critical service is running. Ex: apache2
    """
    service = 'apache2'  # Example service, change as needed
    result = subprocess.run(['systemctl', 'is-active', service], capture_output=True, text=True)
    if result.stdout.strip() != 'active':
        print(f"{service} is down!")
    else:
        print(f"{service} is running normally.")
    update_stat("time_based_service_health_check")

# 15. Temperature Monitoring
@log_job("Temperature Monitoring", "Monitor CPU/GPU temperatures via sensors")
def temperature_monitoring():
    """
    Uses psutil to read temperature sensors. If available, print's each sensor's temperature.
    """
    temps = psutil.sensors_temperatures() if hasattr(psutil, 'sensors_temperatures') else {}
    if temps:
        for name, entries in temps.items():
            for entry in entries:
                print(f"Sensor: {name}, Label: {entry.label}, Temp: {entry.current}°C")
    else:
        print("No temperature sensors found.")
    update_stat("time_based_temperature_monitoring")

# 16. Intentional Error for demo purposes
@log_job("time_based_intentional_error", "Fails intentionally", file_type="N/A")
def force_error():
    raise ValueError("This is a test error for demo purposes.")