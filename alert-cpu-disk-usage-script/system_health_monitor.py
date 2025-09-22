import psutil
import datetime

CPU_THRESHOLD = 80  
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 90 
PROCESS_THRESHOLD = 300  


LOG_FILE = "system_health.log"

def log_alert(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} - ALERT: {message}"
    print(log_message)
    with open(LOG_FILE, "a") as f:
        f.write(log_message + "\n")

def check_cpu():
    usage = psutil.cpu_percent(interval=1)
    if usage > CPU_THRESHOLD:
        log_alert(f"High CPU usage detected: {usage}%")

def check_memory():
    memory = psutil.virtual_memory()
    if memory.percent > MEMORY_THRESHOLD:
        log_alert(f"High memory usage detected: {memory.percent}%")

def check_disk():
    disk = psutil.disk_usage('/')
    if disk.percent > DISK_THRESHOLD:
        log_alert(f"High disk usage detected: {disk.percent}%")

def check_processes():
    num_processes = len(psutil.pids())
    if num_processes > PROCESS_THRESHOLD:
        log_alert(f"High number of running processes: {num_processes}")

if __name__ == "__main__":
    check_cpu()
    check_memory()
    check_disk()
    check_processes()

